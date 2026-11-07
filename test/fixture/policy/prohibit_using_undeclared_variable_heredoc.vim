let s:lines =<< END
text
END
echo s:lines

function! s:F() abort
  let l:lines =<< trim END
text
END
  return l:lines
endfunction
