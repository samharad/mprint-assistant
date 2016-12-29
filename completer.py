import readline
import sys
import os

class Completer:
  vocab_list = None

  # def __init__(self, vocab_list_in = None):
    # self.vocab_list = vocab_list_in

  def set_vocab_list(self, vocab_list_in = None):
    self.vocab_list = vocab_list_in
    readline.parse_and_bind('tab: complete')
    readline.set_completer(self.completer)

  def set_path_completion(self):
    self.vocab_list = None
    readline.parse_and_bind('tab: complete')
    readline.set_completer(self.completer)
    
  def deactivate(self):
    vocab_list = None
    readline.parse_and_bind('tab: self-insert')

  def list_from_path(self, path):
    if path.startswith(os.path.sep) or path.startswith('~'): # Absolute path 
      basedir = os.path.dirname(os.path.expanduser(path))
      contents = os.listdir(basedir)
      contents = [os.path.join(basedir, d) for d in contents]
    else: # Relative path
      contents = os.listdir(os.curdir) 
    contents = [d + os.path.sep if os.path.isdir(d) else d for d in contents]
    return contents

  def completer(self, text, state):
    if self.vocab_list:
      options = [x for x in self.vocab_list if x.startswith(text)]
      return options[state]
    options = [x for x in self.list_from_path(text) if x.startswith(os.path.expanduser(text))]
    return options[state]

  @staticmethod
  def set_no_complete():
    readline.set_completer(None)
    readline.parse_and_bind('tab: self-insert')

def readline_init():
  readline.parse_and_bind('tab: complete')
  readline.set_completer_delims('\t\n`!@#$%^&*()-=+[{]}\\|;:\'",<>?')

