from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy_registry import register_policy
from vint.linting.policy import _ftplugin


@register_policy
class ProhibitMissingUndoFtplugin(AbstractPolicy):
    description = 'Set b:undo_ftplugin to undo buffer-local settings, mappings and commands'
    reference = ':help undo_ftplugin'
    level = Level.WARNING


    def listen_node_types(self):
        return [NodeType.TOPLEVEL]


    def is_valid(self, node, lint_context):
        if not _ftplugin.is_ftplugin(lint_context):
            return True

        if not any(_changes_buffer(excmd) for excmd in _ftplugin.excmd_nodes(node)):
            return True

        return _ftplugin.mentions(node, 'undo_ftplugin')


def _changes_buffer(excmd_node):
    if _ftplugin.command_name(excmd_node) == 'setlocal':
        return True

    for check in (_ftplugin.is_mapping_definition, _ftplugin.is_command_definition):
        is_definition, is_buffer_local = check(excmd_node)
        if is_definition and is_buffer_local:
            return True

    return False
