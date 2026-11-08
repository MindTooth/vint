setlocal commentstring=#\ %s
nnoremap <LocalLeader>x :echo 1<CR>
nmap <Buffer> <LocalLeader>y :echo 2<CR>
command! Foo echo 1
command! -nargs=0 -buffer Bar echo 2
map
nunmap <LocalLeader>z
