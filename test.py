from __future__ import print_function
try:
    import msvcrt
    # def key_pressed():
    #   return msvcrt.kbhit()
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
    # import select
    # import tty
    # import termios
    # import atexit

    # def key_pressed():
    #     return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    def read_key():
        return sys.stdin.read(1)
    # def restore_settings():
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    # atexit.register(restore_settings)
    # old_settings = termios.tcgetattr(sys.stdin)
    # tty.setcbreak(sys.stdin.fileno())
  except:
    raise Exception("Can't deal with your keyboard!")
        

# if __name__ == "__main__":
import threading
import time
import os
lock = threading.Lock()

def cls_print(str):
    if os.name == 'posix':
      _ = os.system('clear')
    else:
      _ = os.system('cls')
    print(str)

def take_input():
    inp = ''
    while True:
      c = read_key()
      if c == '\n':
        with lock:
          cls_print(inp)
        inp = ''
        continue
      if ord(c) == 127:
        inp = inp[:-1]
      else:
        inp += c
      with lock:
        cls_print(inp)

threading.Thread(target=take_input, daemon=True).start()

t = 0
while t < 10:
  time.sleep(1)
  t = t + 1
print('TIME OUTTTTTTTTTTTTT')
