import argparse
import sys

# Takes in a list of dictionaries, a prompt, and any number of keys,
# prints nice columns from the lists along with selection indexes, 
# prompts user for a selection and then returns that dictionary
# keysToPrint is a tuple
def getSelection(list, prompt, *keysToPrint):
  if not list:
    return None

  # Okay, we need to get len(max(values of all dicts ar key)) for ea. key
  keyMaxLens = {}
  for key in keysToPrint:
    keyMaxLens[key] = len(str(key))
    for dict in list:
      if len(str(dict[key])) > keyMaxLens[key]:
        keyMaxLens[key] = len(str(dict[key]))

  INDEX_WIDTH = 6
  print("".join('INDEX'.ljust(INDEX_WIDTH))),
  for key in keysToPrint:
    print("".join(key.upper().ljust(keyMaxLens[key]+2))),
  print('')
  for i, dict in enumerate(list):
    print("".join(('[' + str(i) + ']').ljust(INDEX_WIDTH))),
    for key in keysToPrint:
      print("".join(str(dict[key]).ljust(keyMaxLens[key]+2))),
    print('')

  input = raw_input(prompt + ': ')
  try:
    dict = list[int(input)]
    return dict
  except:
    return None

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
                      nargs=2,
                      action='store',
                      required=False,
                      help='Print only pages within range; specify as comma-separated list of pages/ranges of pages denoted with \'-\'')
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
  args = parser.parse_args()
  return args












