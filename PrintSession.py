import requests
from settings import webloginBaseURL, userBaseURL, guestBaseURL
import requests
import json
from getpass import getpass

class PrintSessionClass(requests.Session):
  def __init__(self):
    requests.Session.__init__(self)
    self.get(webloginBaseURL)
    self.post(webloginBaseURL, 
              data={'login':raw_input('Enter username: '), 
              'password':getpass(prompt='Enter password: ')})
    