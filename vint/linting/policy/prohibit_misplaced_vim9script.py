from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy_registry import register_policy


@register_policy
class ProhibitMisplacedVim9script(AbstractPolicy):
    description = 'vim9script must be the first command in a script (E1039)'
    reference = ':help vim9-mix'
    level = Level.ERROR


    def listen_node_types(self):
        return [NodeType.VIM9SCRIPT]


    def is_valid(self, node, lint_context):
        parent = lint_context['stack_trace'][-1]

        # Inside a block or function (E1038, E1039).
        if NodeType(parent['type']) is not NodeType.TOPLEVEL:
            return False

        for sibling in parent['body']:
            if sibling is node:
                return True
            if not _runs_no_command(sibling):
                return False

        return True


def _runs_no_command(node):
    """ Whether node can precede vim9script: a comment, or the vim9-mix pattern
    `if ... finish endif`, where either the body is skipped or Vim stops at :finish.
    """
    node_type = NodeType(node['type'])

    if node_type is NodeType.COMMENT:
        return True

    if node_type is not NodeType.IF or node['elseif'] or node['else_']:
        return False

    commands = [n for n in node['body'] if NodeType(n['type']) is not NodeType.COMMENT]
    return bool(commands) and _is_finish(commands[-1])


def _is_finish(node):
    if NodeType(node['type']) is not NodeType.EXCMD:
        return False
    return node['ea']['cmd'].get('name') == 'finish'
