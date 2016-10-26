from settings import webloginBaseURL, userBaseURL, guestBaseURL
import requests
import json
import subprocess
from getpass import getpass

def createSession():
  session = requests.Session()
  session.get(webloginBaseURL)
  session.post(webloginBaseURL, data={'login':raw_input('Enter username: '), 'password':getpass(prompt='Enter password: ')})
  return session

def main():
  session = createSession()
  areasResponse = session.get(userBaseURL + 'areas')
  assert areasResponse.json()["role"] == "user"
  print("test_createSession passed!")

if __name__ == "__main__":
    main()