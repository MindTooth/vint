vim9script
import './other.vim'
export def Add(a: number, b: number = 2): number
  var sum: number = a + b
  final shifted = sum << 1 >> 1
  return shifted
enddef
