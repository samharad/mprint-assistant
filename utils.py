import argparse
import sys

def getSelectionFromListOfDicts(list, *keysToPrint):
  if not list:
    return None

  # TODO should calculate neccessary widths; MUST respond to input
  colWidths = []
  print("{:<6}".format('Index')),
  for key in keysToPrint:
    print("{:40}".format(key.capitalize())),
  print('')
  for i, dict in enumerate(list):
    print("{:<6}".format('[' + str(i) + ']')),
    for key in keysToPrint:
      print("{:40}".format(dict[key])),
    print('')
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












