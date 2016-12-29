from utils import getSelection

myList = [{'a':1, 'b':2, 'c':3}, 
          {'a':10, 'b':20, 'c':3000000}, 
          {'a':234124, 'b':2352, 'c':123123123123123123}]
myDict = getSelection(myList, "Select your dictiory", 'a', 'b', 'c')
print(myDict)