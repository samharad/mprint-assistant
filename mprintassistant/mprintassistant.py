#! /usr/bin/env python

from .printsession import PrintSession
from .document import Document
from colorama import init as colorama_init

# TODO
# Confirm print with y/n -- system for going back
# Test floor code flags -- add more shortcut flags -- try to minimize the minimum input
  # flag to bypass confirmation if all args provided as flags
  # flag for color printing, tabloid flag
  # building specifier flag, and floor number? 
# Add way to print code cheat sheet?
# Compatibility checks with venv, then package it
# Restructure completer so calling is more simple -- completer.set_file_complete, completer.set_list_complete(list) 
  # Maybe don't need instances, just static
# Verify cannot print directory
# Handle lack of internet connection
  # If the response is not decodeable, cannot do .json()['result']


def main(): 
  # Lets colored output work on Windows
  colorama_init()

  # Create new session; authenticates, populates menu
  session = PrintSession()

  # Determine printer
  session.determineDestination()

  # Determine documents
  session.determineDocs()

  # Print documenrs
  session.printDocs()


# if __name__ == "__main__":
  # main()
