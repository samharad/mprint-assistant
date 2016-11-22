from settings import webloginBaseURL, userBaseURL, guestBaseURL  # Base URLs
import requests # Request library for interacting with API
from getpass import getpass # Allows password entry
from Document import Document
from fuzzywuzzy import fuzz
from utils import getSelectionFromListOfDicts

import sys
import json
import os

class PrintSession:
  
  # A printSession has a requestsSession for communicating with API
  session = requests.Session()

  # A print session has a building menu 
  buildings = None
  # A print session has a floors menu (populated after building selection)
  floors = None
  # A print session has a queues menu (populated after floor selection)
  queues = None

  # Building obj for user's desired building
  building = None
  # Floor obj for user's desired floor; within building 
  floor = None
  # Queue obj for user's desired floor
  queue = None

  # Print session has list of DocumentClass
  # Each doc has filepath, parameters
  documents = []

  # Dictionary; Print session has command line arguments:
  # building 
  # noscale
  # documents ------- list
  # copies ---------- list
  # floorId
  # one
  # range ------------ list
  # short
  # landscape
  sysArgs = None

  def __init__(self):
    # Populates buildings menu
    responseBuildings = self.session.get(guestBaseURL + 'buildings')
    if responseBuildings.status_code != 200:
      sys.exit('Could not retrieve buildings')
    self.buildings = responseBuildings.json()

    # Populates floors menu
    responseFloors = self.session.get(guestBaseURL + 'floors')
    if responseFloors.status_code != 200:
      sys.exit('Could not retrieve floors')
    self.floors = responseFloors.json()

  def interpretSysArgs(self):
    # Sets Document params based no sys args
    if self.sysArgs['landscape']:
      Document.params['orientation'] = Document.LANDSCAPE
    if self.sysArgs['one']:
      Document.params['sides'] = Document.ONE_SIDED
    if self.sysArgs['short']:
      Document.params['sided'] = Document.TWO_SIDED_SHORT
    if self.sysArgs['noscale']:
      Document.params['scale'] = False;
    if self.sysArgs['range']: # TODO ERROR CHECKING
      Document.params['range'] = self.sysArgs['range']
    if self.sysArgs['copies']: # TODO error checking
      Document.params['copies'] = self.sysArgs['copies']

    # Checks that documents exist and appends them to documents 
    if self.sysArgs['documents']:
      for pathIn in self.sysArgs['documents']:
        if not os.path.isfile(pathIn):
          sys.exit('\'' + pathIn + '\' cannot be found.')
        self.documents.append(Document(pathIn))

    if self.sysArgs['floorId']:
      self.floor = filter(lambda dict: dict['id'] == self.sysArgs['floorId'], self.floors['result'])[0]
      if not self.floor:
        sys.exit('Could not find specified floor ID.')
      # TODO should error check this? theoretically fine
      print(self.floor)
      buildingId = self.floor['building_id']
      self.building = filter(lambda dict: dict['id'] == buildingId, self.buildings['result'])[0]

  def authenticate(self):
    response = self.session.get(webloginBaseURL)
    response = self.session.post(webloginBaseURL, 
                                 data={'login':raw_input('Enter username: '), 
                                 'password':getpass(prompt='Enter password: ')}, 
                                 allow_redirects=False)

    # Redirect code means successful login
    if response.status_code != 302:
      sys.exit('Invalid credentials.')

  def setSysArgs(self, sysArgsIn):
    self.sysArgs = sysArgsIn

  def determineBuilding(self):
    possibleBuildings = []
    while not self.building:
      inputString = raw_input('Enter building name: ')
      for dictionary in self.buildings['result']:
        if fuzz.partial_ratio(inputString.lower(), dictionary['name'].lower()) == 100:
          possibleBuildings.append(dictionary)
      self.building = getSelectionFromListOfDicts(possibleBuildings, 'name', 'id')


  def determineDestination(self):
    if not self.building:
      self.determineBuilding();


