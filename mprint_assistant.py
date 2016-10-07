import requests
import json
import os
from getpass import getpass


guestBase ='http://mprint.umich.edu/api/'
userBase ='https://mprint.umich.edu/api/'
weblogin = 'https://weblogin.umich.edu/'

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
	for i in floors.json()["result"]:
		print("Level: " + i["level"] + "  Name: " + i["name"])
	level = raw_input('Enter level: ')
	for i in floors.json()["result"]:
		for key, value in i.iteritems():
			if value == level:
				floorId = i["id"]
	return floorId

def getQueues(session, buildingId, floor):
	queues = session.get(userBase + 'queues', params={'building':buildingId, 'floor':floor})
	return queues.json()["result"]

def printQueues(queue):
	for i, queue in enumerate(queue):
		print("[{}]   {}    {}".format(i, queue["display_name"], queue["location"]))

def printDoc(session, queues, queueChoice, docPath):
	# printStatus = session.post(userBase + 'jobs', params={'queue':queues[queueChoice]["name"], 'filepath':docPath})
	file = {'file': open('blank.docx', 'rb')}
	printStatus = session.post(userBase + 'jobs', files=file, params={'queue':queues[queueChoice]["name"]})
	print printStatus.text

def authenticateSession():
	session = requests.Session()
	session.get(weblogin)
	session.post(weblogin, data={'login':raw_input('Enter username : '), 'password':getpass(prompt='Enter password: ')})
	return session

def main():
	session = authenticateSession()
	buildingId = getBuilding(session)
	floorId = getFloors(session, buildingId)
	queues = getQueues(session, buildingId, floorId)
	printQueues(queues)
	
	queueChoice = int(raw_input('Enter queue number: '))
	docPath = raw_input('Enter doc path: ')
	printDoc(session, queues, queueChoice, docPath)



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
