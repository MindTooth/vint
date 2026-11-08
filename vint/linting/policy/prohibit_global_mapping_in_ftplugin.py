from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy_registry import register_policy
from vint.linting.policy import _ftplugin


@register_policy
class ProhibitGlobalMappingInFtplugin(AbstractPolicy):
    description = 'Use <buffer> mappings and -buffer commands in filetype plugins'
    reference = ':help ftplugin-special'
    level = Level.WARNING


    def listen_node_types(self):
        return [NodeType.EXCMD]


    def is_valid(self, node, lint_context):
        if not _ftplugin.is_ftplugin(lint_context):
            return True

        for check in (_ftplugin.is_mapping_definition, _ftplugin.is_command_definition):
            is_definition, is_buffer_local = check(node)
            if is_definition:
                return is_buffer_local

        return True
