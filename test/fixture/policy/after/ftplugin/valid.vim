setlocal shiftwidth=2
let b:undo_ftplugin = get(b:, 'undo_ftplugin', '') . ' | setlocal shiftwidth<'
