import readline
import sys
import os

def list_contents(path):
  if path.startswith(os.path.sep) or path.startswith('~'): # Absolute path 
    basedir = os.path.dirname(os.path.expanduser(path))
    contents = os.listdir(basedir)
    contents = [os.path.join(basedir, d) for d in contents]
  else: # Relative path
    contents = os.listdir(os.curdir) 
  contents = [d + os.path.sep if os.path.isdir(d) else d for d in contents]
  return contents

def completer(text, state):
  options = [x for x in list_contents(text) if x.startswith(os.path.expanduser(text))]
  return options[state]

def completer_init():
  readline.parse_and_bind('tab: complete')
  readline.set_completer(completer)
  readline.parse_and_bind("bind ^I rl_complete")
  readline.set_completer_delims(' \t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')

# def main():
  # completer_init()
  # while True:
    # last_string = raw_input('? ')
    # print 'Last input:', last_string

# if __name__ == "__main__":
  # main()


