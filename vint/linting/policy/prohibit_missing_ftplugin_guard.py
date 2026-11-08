from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy_registry import register_policy
from vint.linting.policy import _ftplugin


@register_policy
class ProhibitMissingFtpluginGuard(AbstractPolicy):
    description = 'Filetype plugins should finish early when b:did_ftplugin exists'
    reference = ':help write-filetype-plugin'
    level = Level.WARNING


    def listen_node_types(self):
        return [NodeType.TOPLEVEL]


    def is_valid(self, node, lint_context):
        if not _ftplugin.is_ftplugin(lint_context):
            return True

        # after/ftplugin scripts must not check it: the main ftplugin already set it.
        if _ftplugin.is_after_ftplugin(lint_context):
            return True

        # `runtime! ftplugin/other.vim` delegates the guard to the sourced ftplugin.
        if any(_ftplugin.command_name(excmd) == 'runtime' and 'ftplugin/' in excmd['str']
               for excmd in _ftplugin.excmd_nodes(node)):
            return True

        return _ftplugin.mentions(node, 'did_ftplugin')
