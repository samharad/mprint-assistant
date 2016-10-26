#!/usr/bin/env python

from settings import webloginBaseURL, userBaseURL, guestBaseURL
import requests 
import json
import os
import argparse
import sys
from getpass import getpass
from fuzzywuzzy import fuzz, process


def parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', 
                      '--documents', 
                      nargs='+', 
                      # action='append', 
                      required=False,
                      help='Specify at least one document to be printed')
  parser.add_argument('-f', 
                      '--floorId', 
                      # nargs=1, 
                      action='store', 
                      required=False, 
                      help='Specify floorID of desired printer, if known')
  parser.add_argument('-l', 
                      '--landscape', 
                      # nargs=None, 
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
                      # action='append',
                      required=False,
                      help='Specify copies to be printed of each document in corresponding order')
  parser.add_argument('-o', 
                      '--one',
                      # nargs=None,
                      action='store_const', 
                      const=True, 
                      required=False,
                      help='One-sided printing')
  parser.add_argument('-s', 
                      '--short',
                      # nargs=None,
                      action='store_const', 
                      const=True, 
                      required=False,
                      help='Double-sided short-edge printing')
  parser.add_argument('-n',
                      '--noscale',
                      # nargs=None,
                      action='store_const',
                      const=True,
                      required=False, 
                      help='Do not scale to page (default is fit to page)')
  args = parser.parse_args()
  return args

def getBuilding(session):
  building = raw_input('Enter building: ')
  buildings = session.get(userBaseURL + 'buildings')
  if buildings.status_code != 200:
    raise ApiError('GET /areas/ {}'.format(buildings.stataus_code))
  buildingsResult = buildings.json()["result"]
  
  fuzzRatios = []
  highestRatio = 0
  numEquallyHigh = 0
  for dictionary in buildingsResult[:]:
    # ratio = fuzz.token_sort_ratio(dictionary['name'].lower(), building.lower()) 
    ratio = fuzz.partial_token_sort_ratio(dictionary['name'].lower(), building.lower())
    if ratio >= 35:
      dictionary['ratio'] = ratio
    else:
      buildingsResult.remove(dictionary)
  if len(buildingsResult) == 0:
    print("No buildings found")
    return 0
  buildingsResultOrdered = sorted(buildingsResult, key = lambda dictionary: dictionary['ratio'], reverse=True)
  for i, dictionary in enumerate(buildingsResultOrdered):
    # print('{} {}'.format(dictionary['name'], dictionary['ratio'])) 
    print ("[" + str(i) + "]").ljust(5) + str(dictionary['name']) 
  buildingId = int(raw_input("Enter building number: "))
  return buildingsResultOrdered[buildingId]['id']

def getFloors(session, buildingId):
  floors = session.get(userBaseURL + 'floors', params={'buildingId':buildingId})
  colWidth = max(len(i["level"]) for i in floors.json()["result"]) + len("[]") + 2
  for i in floors.json()["result"]:
    print ("[" + i["level"] + "]").ljust(colWidth) + i["name"]
  level = raw_input('Enter level: ')
  for i in floors.json()["result"]:
    for key, value in i.iteritems():
      if value == level:
        floorId = i["id"]
  return floorId

def getQueues(session, floor):
  queues = session.get(userBaseURL + 'queues', params={'floor':floor})
  return queues.json()["result"]

def printQueues(queue):
  if (not queue):
    print "No queues found"
    sys.exit()
  else:
    colWidth0 = max(len(str(i)) for i, entry in enumerate(queue)) + len("[]") + 2
    colWidth1 = max(len(i["display_name"]) for i in queue) + 2
    for i, queue in enumerate(queue):
      # print("[{}]   {}    {}".format(i, queue["display_name"], queue["location"]))
      print ("[" + str(i) + "]").ljust(colWidth0) + queue["display_name"].ljust(colWidth1) + queue["location"]

def printDocs(session, queues, queueChoice, args):
  # printStatus = session.post(userBase + 'jobs', params={'queue':queues[queueChoice]["name"], 'filepath':docPath})
  # file = {'file': open('blank.docx', 'rb')}
  # printStatus = session.post(userBase + 'jobs', files=file, params={'queue':queues[queueChoice]["name"]})
  # print printStatus.text

  if not args.documents:
    args.documents = []
    args.documents.append(raw_input('Enter document path: '))

  for i, doc in enumerate(args.documents):
    file = {'file': open(doc, 'rb')}
    params = {}
    if args.landscape:
      params['orientation'] = 'landscape'
    if args.range and args.range[i] != 'all':
      params['range'] = args.range[i]
    if args.copies:
      params['copies'] = args.copies[i]
    if args.one:
      params['sides'] = 'one-sided'
    if args.short:
      params['sides'] = 'two-sided-short-edge'
    if args.noscale:
      params['scale'] = 'off'

    printStatus = session.post(userBaseURL + 'jobs', files=file, params={'queue':queues[queueChoice]["name"]})
    print printStatus.text

def createSession():
  session = requests.Session()
  session.get(webloginBaseURL)
  session.post(webloginBaseURL, data={'login':raw_input('Enter username: '), 'password':getpass(prompt='Enter password: ')})
  return session

def main():
  # Parse command line flags
  args = parse()

  # Begin session
  session = createSession()
  
  if not args.floorId:
    buildingId = 0
    while not buildingId:
      buildingId = getBuilding(session)
    floorId = getFloors(session, buildingId)
  else:
    floorId = args.floorId
  queues = getQueues(session, floorId)
  printQueues(queues)
  
  queueChoice = int(raw_input('Enter queue number: '))
  printDocs(session, queues, queueChoice, args)



if __name__ == "__main__":
    main()


