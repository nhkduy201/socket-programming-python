from __future__ import print_function
try:
    import msvcrt
    def read_key():
      key = msvcrt.getch()
      try:
        result = str(key, encoding="utf8")
      except:
        result = key    
      return result
except:
  try:
    import sys
    def read_key():
        return sys.stdin.read(1)
  except:
    raise Exception("Can't deal with your keyboard!")