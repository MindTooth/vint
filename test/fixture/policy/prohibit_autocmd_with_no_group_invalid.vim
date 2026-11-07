au BufNewFile * echo 'foo'

aug my_group
aug end

autocmd BufNewFile * echo 'foo'
autocmd BufNewFile,BufRead * echo 'foo'
autocmd TextYankPost * echo 'foo'
