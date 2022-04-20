## Heriberto Hurtado | Jorge Vega
## Foxconn
#Script To get the path of a specific log on the CTP server..

#Selenium Library, Used to work on Web
from selenium import webdriver
PATH = "C:\Driver\chromedriver.exe"

print("\n ---------------------------------------------------------------------------")
print("List of projects:")
print("\n 1.-Thor\n","2.-CTO-ATO\n","3.-Oracle")
print("------------------------------------------------------------------------------")

projectSelected = ""                #Variables Declaration
listOfTesters = []
counterOfTester = 0
counterOfLogs = 0
listOfPossibleResults = []

project = input("Please Select a project: ")            #User Interactions (Select a Number of Project)
serial = input("\nPlease Enter a Serial Number: ")      #User Interaction (Enter a Serial Number)

#To decrease the time, the testers are categorized for each project... 
Thor = ["gdlctp7034/", "gdlctp7065/", "gdlctp7033/", "gdlctp7053/", "gdlctp7070/", "gdlctp7035/", "gdlctp7036/", "gdlctp7068/" ]
CTOATO = ["gdlctp70110/", "gdlctp7027/", "gdlctp7031/", "gdlctp7032/"]
Oracle = ["gdlctp7013/","gdlctp7042/","gdlctp7061/","gdlctp7062/","gdlctp7122/","gdlctp7124/","gdlctp7126/",
          "gdlctp7128/","gdlctp7043/","gdlctp7044/","gdlctp7051/","gdlctp7052/","gdlctp7055/","gdlctp7057/","gdlctp7058/","gdlctp7059/"]

if project == "1":
    projectSelected = Thor
elif project == "2":
    projectSelected = CTOATO
elif project == "3":
        projectSelected = Oracle
        
driver = webdriver.Chrome(PATH)  #Create an instance to use the driver file, And open the Browser
driver.get("http://172.17.70.161/ctplogs/") # Using the driver, use the route (link) to try to connect in the browser

testers = driver.find_elements_by_tag_name("a") # Gonna create a list of elements localized by tag
                                                # In this case the server use the tag "a" to write the number of tester                                        
for tester in testers:                          # iterate each tester of the list
    tester_name = tester.text                   # gonna save the tester name as a string
    counterOfTester = counterOfTester + 1       # The page have some differents elements as, "Return" "Name"...
    if counterOfTester > 5:                     # we gonna avoid these elements
        listOfTesters.append(tester_name)       # And save the names of testers in an array
        
for tester in projectSelected:                          # Using a specific project as a parameter
    driver.get("http://172.17.70.161/ctplogs/" + tester)    ## We gonna search inside of each tester that the project has
    counterOfLogs = counterOfLogs + 1
    logsResults = driver.find_elements_by_tag_name("a")     # Gonna use the same method, use the tags "a"
    
    for log in logsResults:
        logFile = log.text
        counterOfLogs = counterOfLogs + 1
        if counterOfLogs > 5:
            if serial in logFile:                                         # Compare, if the text of the tag "a" contains the serial number
                result = "http://172.17.70.161/ctplogs/"+ tester + logFile #Gonna save the Link with the tester and the name 
                listOfPossibleResults.append(result)                       # Inside of a list
                     
#And then Print the results of all the LogFiles that contain the serial number searched
print("----------------------------------------------------------------------------------------")
print("Los resultados de las pruebas son:")
for result in listOfPossibleResults:
    print (result)
print("----------------------------------------------------------------------------------------")