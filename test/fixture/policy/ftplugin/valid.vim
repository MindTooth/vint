if exists('b:did_ftplugin')
  finish
endif
let b:did_ftplugin = 1

setlocal commentstring=#\ %s
nnoremap <buffer> <LocalLeader>x :echo 1<CR>
nnoremap <silent><buffer> <LocalLeader>y :echo 2<CR>
silent! nnoremap <buffer><LocalLeader>z :echo 3<CR>
noremap <SID>Helper :echo 4<CR>
nnoremap <Plug>(FooBar) :echo 5<CR>
command! -buffer Foo echo 1

let b:undo_ftplugin = 'setlocal commentstring<'
      \ . ' | nunmap <buffer> <LocalLeader>x'
      \ . ' | nunmap <buffer> <LocalLeader>y'
      \ . ' | nunmap <buffer> <LocalLeader>z'
      \ . ' | delcommand Foo'
