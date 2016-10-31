from printSession import PrintSessionClass
import utils

def main(): 
  session = PrintSessionClass(utils.parse())
  session.determineQueue()
  session.determineDocs()
  session.printDocs()





if __name__ == "__main__":
  main()