""" Helpers shared by the filetype plugin policies (see :help ftplugin-special). """
import re
from pathlib import Path

from vint.ast.node_type import NodeType
from vint.ast.traversing import traverse

MAP_COMMAND = re.compile(r'^[nvxsoilct]?(?:nore)?map$')
# Vim strips these one by one, with optional white space between them (:help :map-arguments).
MAP_SPECIAL_ARG = re.compile(r'^\s*<(buffer|nowait|silent|special|script|expr|unique)>', re.I)
# <SID>/<Plug> left-hand sides name a mapping rather than bind a key, so they do not leak.
MAP_NAMED_LHS = re.compile(r'^<(?:sid|plug)>', re.I)


def _path_parts(lint_context):
    return Path(str(lint_context['lint_target'].path)).parts


def is_ftplugin(lint_context):
    return 'ftplugin' in _path_parts(lint_context)


def is_after_ftplugin(lint_context):
    parts = _path_parts(lint_context)
    return any(a == 'after' and b == 'ftplugin' for a, b in zip(parts, parts[1:]))


def command_name(excmd_node):
    # ea.cmd is empty for line jump commands such as `:1`.
    return excmd_node['ea']['cmd'].get('name')


def command_arg_string(excmd_node):
    """ The text after the command word, skipping modifiers such as `silent!`. """
    name = command_name(excmd_node) or ''
    text = excmd_node['str']
    for match in re.finditer(r'\S+', text):
        word = match.group().rstrip('!')
        if word and name.startswith(word):
            return text[match.end():]
    return ''


def is_mapping_definition(excmd_node):
    """ Returns (is_definition, is_buffer_local) for :map family commands. """
    if not MAP_COMMAND.match(command_name(excmd_node) or ''):
        return False, False
    args = command_arg_string(excmd_node)
    special_args = []
    match = MAP_SPECIAL_ARG.match(args)
    while match:
        special_args.append(match.group(1).lower())
        args = args[match.end():]
        match = MAP_SPECIAL_ARG.match(args)
    lhs_and_rhs = args.split(None, 1)
    # Fewer than {lhs} {rhs} means listing mappings, not defining one.
    if len(lhs_and_rhs) < 2 or MAP_NAMED_LHS.match(lhs_and_rhs[0]):
        return False, False
    return True, 'buffer' in special_args


def is_command_definition(excmd_node):
    """ Returns (is_definition, is_buffer_local) for :command. """
    if command_name(excmd_node) != 'command':
        return False, False
    args = command_arg_string(excmd_node).split()
    attrs = [arg.lower() for arg in args if arg.startswith('-')]
    has_name = len(args) > len(attrs)
    return has_name, '-buffer' in attrs


def mentions(toplevel_node, name):
    """ Whether an identifier, string or unparsed command mentions `name`, e.g. b:did_ftplugin. """
    found = []

    def on_enter(node):
        node_type = NodeType(node['type'])
        if node_type in (NodeType.IDENTIFIER, NodeType.STRING) and name in node['value']:
            found.append(node)
        # Vim9 assignments without :var (`b:undo_ftplugin = ...`) are not parsed yet.
        elif node_type is NodeType.EXCMD and name in node['str']:
            found.append(node)

    traverse(toplevel_node, on_enter=on_enter)
    return bool(found)


def excmd_nodes(toplevel_node):
    nodes = []

    def on_enter(node):
        if NodeType(node['type']) is NodeType.EXCMD:
            nodes.append(node)

    traverse(toplevel_node, on_enter=on_enter)
    return nodes
