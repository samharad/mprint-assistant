import requests
import json
import os
import argparse
import sys
from getpass import getpass


guestBase ='http://mprint.umich.edu/api/'
userBase ='https://mprint.umich.edu/api/'
weblogin = 'https://weblogin.umich.edu/'

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
	print args
	return args

def getBuilding(session):
	building = raw_input('Enter building: ')
	buildings = session.get(userBase + 'buildings')
	if buildings.status_code != 200:
		raise ApiError('GET /areas/ {}'.format(buildings.stataus_code))
	buildingId = (item for item in buildings.json()["result"] if item["name"].lower() == building.lower()).next()["id"]
	return buildingId

def getFloors(session, buildingId):
	floors = session.get(userBase + 'floors', params={'buildingId':buildingId})
	# TODO format in columns
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
	queues = session.get(userBase + 'queues', params={'floor':floor})
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

		printStatus = session.post(userBase + 'jobs', files=file, params={'queue':queues[queueChoice]["name"]})
		print printStatus.text

def authenticateSession():
	session = requests.Session()
	session.get(weblogin)
	session.post(weblogin, data={'login':raw_input('Enter username : '), 'password':getpass(prompt='Enter password: ')})
	return session

def main():
	# Parse command line flags
	args = parse()

	# Begin session
	session = authenticateSession()
	
	if not args.floorId:
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



# with open('/tmp/cookies.txt', 'r') as cookies:
# 	cooks = cookies.read().replace('\t', '\n')

# print cooks
# cooksList = cooks.split('\n')
# print cooksList


# buildings = getBuildings()
# buildings_result = json.dumps(json.loads(buildings.text))
# print buildings_result

# building = raw_input('Enter building: ')
# #buildingId = buildings["result"]
# buildingId = (item for item in buildings.json()["result"] if item["name"].lower() == building.lower()).next()["id"]
# print buildingId

# base = 'https://mprint.umich.edu/api/queues/?all'

# queues = requests.get(base, cookies={'cosign':cooksList[-1]})
# print queues.text
# #queues_result = json.dumps(json.loads(queues.text))
# #print queues_result
