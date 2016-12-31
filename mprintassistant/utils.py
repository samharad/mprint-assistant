from __future__ import print_function # So that python 2.6+ can use the end= syntax
import argparse
import sys
from builtins import input
from termcolor import colored

# Takes in a list of dictionaries, a prompt, and any number of keys,
# prints nice columns from the lists along with selection indexes, 
# prompts user for a selection and then returns that dictionary
# keysToPrint is a tuple
def getSelection(prompt_string, list, *keysToPrint):
  if not list:
    return None

  # Okay, we need to get len(max(values of all dicts ar key)) for ea. key
  keyMaxLens = {}
  for key in keysToPrint:
    keyMaxLens[key] = len(str(key))
    for dict in list:
      if len(str(dict[key])) > keyMaxLens[key]:
        keyMaxLens[key] = len(str(dict[key]))

  INDEX_WIDTH = 5
  print(colored("".join('INDEX'.ljust(INDEX_WIDTH)), attrs=['underline']), end=" ")
  for key in keysToPrint:
    print(colored("".join(key.upper().ljust(keyMaxLens[key])), attrs=['underline']), end=" ")
  print('')
  for i, dict in enumerate(list):
    print("".join(('[' + str(i) + ']').ljust(INDEX_WIDTH)), end=" ")
    for key in keysToPrint:
      print("".join(str(change_01_to_NY(dict[key]).ljust(keyMaxLens[key]))), end=" ")
    print('')

  selection = input(prompt(prompt_string + ': '))
  try:
    selection_index = int(selection)
    if selection_index < 0: return None
    dict = list[selection_index]
    return dict
  except:
    return None

def change_01_to_NY(string):
  if string == '0':
    return 'N'
  elif string == '1':
    return 'Y'
  else:
    return string

def color_by_status(string):
  if 'success' in string: 
    return colored(string, 'green')
  else: 
    return colored(string, 'red')

# Escape sequences used for colors, in combination with readline, break input()
# Since tab completion is more useful than the bold prompt, the bold prompt is nixed
def prompt(string):
  # return colored(string, attrs=['bold'])
  return string

def parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', 
                      '--documents', 
                      nargs='+', 
                      required=False,
                      help='Specify at least one document to be printed')
  parser.add_argument('-f', 
                      '--floorId', 
                      action='store', 
                      required=False, 
                      help='Specify floorID of desired printer, if known')
  parser.add_argument('-b', 
                      '--building',
                      action='store',
                      required=False,
                      help='Specify building of desired printer')
  parser.add_argument('-l', 
                      '--landscape', 
                      action='store_const', 
                      const=True, 
                      required=False, 
                      help='Print document with landscape orientation (portrait is default)')
  parser.add_argument('-r',
                      '--range', 
                      nargs='+',
                      action='store',
                      required=False,
                      help='Print only pages within range; specify as \'x-x y-y z-z...\', one pair for each document')
  parser.add_argument('-c',
                      '--copies', 
                      nargs='+', 
                      required=False,
                      help='Specify copies to be printed of each document in corresponding order')
  parser.add_argument('-o', 
                      '--one',
                      action='store_const', 
                      const=True, 
                      required=False,
                      help='One-sided printing')
  parser.add_argument('-s', 
                      '--short',
                      action='store_const', 
                      const=True, 
                      required=False,
                      help='Double-sided short-edge printing')
  parser.add_argument('-n',
                      '--noscale',
                      action='store_const',
                      const=True,
                      required=False, 
                      help='Do not scale to page (default is fit to page)')
  parser.add_argument('-q',
                      '--quick',
                      action='store_const',
                      const=True,
                      required=False,
                      help='Quick mode: will not ask for confirmation before printing')
  args = parser.parse_args()
  return args

def make_acronym(string):
  return "".join(word[0] for word in string.replace('-', ' ').split() if word[0].isupper())




