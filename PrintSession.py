from settings import webloginBaseURL, userBaseURL, guestBaseURL  # Base URLs
import requests # Request library for interacting with API
from getpass import getpass # Allows password entry
from document import Document
from fuzzywuzzy import fuzz
from utils import getSelection
import completer
import readline

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

  # Print session has list of Document objects
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

    # Populates floors menu with all floors TODO this is unneccessary?
    responseFloors = self.session.get(guestBaseURL + 'floors')
    if responseFloors.status_code != 200:
      sys.exit('Could not retrieve floors')
    self.floors = responseFloors.json()

  def interpretSysArgs(self):
    # Sets Document params based on sys args
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
    readline.set_completer(completer.Completer([x['name'] for x in self.buildings['result']]).completer)
    inputString = raw_input('Enter building name: ')
    for dictionary in self.buildings['result']:
      if fuzz.partial_ratio(inputString.lower(), dictionary['name'].lower()) == 100:
        possibleBuildings.append(dictionary)
    if (len(possibleBuildings) == 1):
      self.building = possibleBuildings[0]
      return
    self.building = getSelection(possibleBuildings, 'Select building', 'name', 'id')

  def determineFloor(self):
    possibleFloors = self.session.get(userBaseURL + 'floors', 
                                      params={'buildingId':self.building['id']}).json()['result']
    self.floor = getSelection(possibleFloors, 'Select floor', 'name', 'id')

  def determineQueue(self):
    possibleQueues = self.session.get(userBaseURL + 'queues', 
                                      params={'floor':self.floor['id']}).json()['result']
    self.queue = getSelection(possibleQueues, 'Select printer', 'display_name', 'model_name')

  def determineDocs(self):
    if not self.documents:
      readline.set_completer(completer.Completer().completer)
      self.documents = raw_input('Enter document paths separated by spaces: ').split()

  def printDocs(self):
    for doc in self.documents:
      self.session.post()

  def determineDestination(self):
    while not self.building:
      self.determineBuilding()
    while not self.floor:
      self.determineFloor()
    while not self.queue:
      self.determineQueue()

