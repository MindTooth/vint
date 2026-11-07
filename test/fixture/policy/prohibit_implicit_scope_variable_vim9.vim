" Vim9 script names have no scope prefix.
vim9script
var count = 0
def Add(a: number): number
  var sum = a + count
  return sum
enddef
echo Add(1)
