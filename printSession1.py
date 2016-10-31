from settings import webloginBaseURL, userBaseURL, guestBaseURL  # Base URLs

class printSession1Class:
  
  # A printSession has a requestsSession 
  # for communicating with API
  session = requests.Session()

  # A print session has a building menu -- 
  # filled in a helper called by the constructor?
  # will be a json()  
  buildings = None

  # Building obj for user's desired building
  building = None
  # Floor obj for user's desired floor; within building 
  floor = None
  # Queue obj for user's desired floor
  queue = None

  # Print session has documents to print; OPTINOAL test doc?
  # SHOULD ea doc be associated with copies, parameters?
  documents = None

  # Print session has command line arguments
  sysArgs = None

  
