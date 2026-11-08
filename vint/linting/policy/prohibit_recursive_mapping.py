import re

from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy.reference.googlevimscriptstyleguide import get_reference_source
from vint.linting.policy_registry import register_policy
from vint.linting.policy import _ftplugin

# A <Plug> mapping can only be reached through a recursive mapping (:help using-<Plug>).
PLUG_RHS = re.compile(r'<plug>', re.I)


@register_policy
class ProhibitRecursiveMapping(AbstractPolicy):
    reference = get_reference_source('MAPPINGS')
    level = Level.STYLE_PROBLEM


    def listen_node_types(self):
        return [NodeType.EXCMD]


    def is_valid(self, node, lint_context):
        """ Whether the mapping is non-recursive, or maps to a <Plug> mapping. """
        mapping = _ftplugin.parse_mapping(node)
        if mapping is None:
            return True

        command = _ftplugin.command_name(node)
        bang = '!' if node['ea'].get('forceit') else ''
        if 'nore' in command:
            return True

        if PLUG_RHS.search(mapping[2]):
            return True

        # <script> only remaps the script's own <SID> mappings (:help :map-<script>).
        if 'script' in mapping[0]:
            return True

        self.description = 'Use `{good}` instead of `{bad}` unless remapping is needed'.format(
            good=_non_recursive_name(command) + bang, bad=command + bang)
        return False


def _non_recursive_name(command):
    # map -> noremap, nmap -> nnoremap, imap -> inoremap, ...
    return command[:-3] + 'noremap'
