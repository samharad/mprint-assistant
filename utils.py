import argparse
import sys

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
                      help='Print only pages within range; specify as a list pairs of integers with only a \'-\' between them, or \'all\' otherwise')
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