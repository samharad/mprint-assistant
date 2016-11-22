from printSession import PrintSession
from Document import Document
import utils
# from CommandInterpreterClass import CommandInterpreterClass

def main(): 
  
  # Create new session
  session = PrintSession()

  # Set sysArgs to arguments
  session.setSysArgs(vars(utils.parse()))
  session.interpretSysArgs()

  # Authenticate session
  session.authenticate()

  session.determineDestination()




if __name__ == "__main__":
  main()