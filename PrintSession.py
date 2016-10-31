import requests
from settings import webloginBaseURL, userBaseURL, guestBaseURL
import requests
import json
from getpass import getpass
from fuzzywuzzy import fuzz
import sys

import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

class PrintSessionClass(requests.Session):

  sysArgs = None
  buildingId = None
  floorId = None
  queueName = None
  documents = []

  
  # Initialize PrintSession; calls parent constructor;
  # initializes sysArgs; authenticates user
  def __init__(self, argsIn):
    requests.Session.__init__(self)
    self.setArgs(argsIn)
    self.get(webloginBaseURL)
    self.post(webloginBaseURL, 
              data={'login':raw_input('Enter username: '), 
              'password':getpass(prompt='Enter password: ')})

  def setArgs(self, argsIn):
    self.sysArgs = argsIn

  def determineDocs(self):
    if not self.sysArgs.documents:
      inputDocs = raw_input('Enter document paths separated by spaces: ')
      self.documents = inputDocs.split()
    else:
      documents = self.sysArgs.focuments

  def printDocs(self):
    for i, doc in enumerate(self.documents):
      file = {'file': open(doc, 'rb')}
      params = {}
      if self.sysArgs.landscape:
        params['orientation'] = 'landscape'
      if self.sysArgs.range and args.range[i] != 'all':
        params['range'] = args.range[i]
      if self.sysArgs.copies:
        params['copies'] = args.copies[i]
      if self.sysArgs.one:
        params['sides'] = 'one-sided'
      if self.sysArgs.short:
        params['sides'] = 'two-sided-short-edge'
      if self.sysArgs.noscale:
        params['scale'] = 'off'

      printStatus = self.post(userBaseURL + 'jobs', files=file, params={'queue':self.queueName}).json()
      print(printStatus['status'])


  def determineQueue(self):
    # should call determine floorId which should call detBuilding if neccessary
    if not self.sysArgs.floorId:
      self.buildingId = self.determineBuilding()
      self.floorId = self.determineFloorId()
    else:
      self.floorId = self.sysArgs.floorId
    queues = self.get(userBaseURL + 'queues', params={'floor':self.floorId}).json()['result']
    if not len(queues):
      print("No queues found")
      sys.exit()
    else:
      colWidth0 = max(len(str(i)) for i, entry in enumerate(queues)) + len("[]") + 2
      colWidth1 = max(len(i["display_name"]) for i in queues) + 2
      for i, queue in enumerate(queues):
        print ("[" + str(i) + "]").ljust(colWidth0) + queue["display_name"].ljust(colWidth1) + queue["location"]
      inputQueueIndex = int(raw_input('Enter queue number: '))
      self.queueName = queues[inputQueueIndex]['name']


  def determineFloorId(self):
    floors = self.get(userBaseURL + 'floors', params={'buildingId':self.buildingId}).json()['result']
    for floor in floors:
      print ("[" + floor['level'] + "]").ljust(5) + floor['name'].ljust(20) + floor['id']
    inputLevel = raw_input('Enter level: ')
    for floor in floors:
      for key, value in floor.iteritems():
        if value == inputLevel:
          floorId = floor['id']
    return floorId

  def determineBuilding(self):
    possibleBuildingIndices = []
    tryAgain = False
    buildings = self.getBuildings()['result']
    while not len(possibleBuildingIndices) or tryAgain:
      possibleBuildingIndices = []
      if not self.sysArgs.building or tryAgain:
        building = raw_input('Enter building: ')
      else:
        building = self.sysArgs.building
      tryAgain = False
      for i, dictionary in enumerate(buildings):
        if fuzz.partial_ratio(building.lower(), dictionary['name'].lower()) == 100:
          possibleBuildingIndices.append(i)

      if len(possibleBuildingIndices) == 1:
        return buildings[possibleBuildingIndices[0]]['id']
      elif len(possibleBuildingIndices) > 0:
        for i, index in enumerate(possibleBuildingIndices):
          print ("[" + str(i) + "]").ljust(5) + buildings[index]['name']
        inputIndex = raw_input("Enter building number (or press return to try again): ")
        if inputIndex == '':
          tryAgain = True
        else:
          inputIndex = int(inputIndex)
          buildingId = possibleBuildingIndices[inputIndex]
      else:
        tryAgain = True
    return buildings[buildingId]['id']

  def getBuildings(self):
    buildings = self.get(userBaseURL + 'buildings')
    if buildings.status_code != 200:
      raise ApiError('GET /areas/ {}'.format(buildings.stataus_code))
    buildingsResult = buildings.json()
    return buildingsResult













