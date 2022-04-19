## Heriberto Hurtado | Jorge Vega
## Foxconn

#Script To get the path of a specific log on the CTP server..

from itertools import count
from selenium import webdriver
print("\n ---------------------------------------------------------------------------")
print("List of projects:")
print("\n 1.-Thor\n","2.-CTO-ATO\n","3.-Oracle")
print("---------------------------------------------------------------------------")
projectSelected = ""
project = input("Please Select a project: ")
serial = input("\nPlease Enter a Serial Number: ")

PATH = "C:\Driver\chromedriver.exe" #Driver File path 
driver = webdriver.Chrome(PATH)  #Create an instance to use the driver file

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

driver.get("http://172.17.70.161/ctplogs/") # Using the driver, use the route (link) to try to connect
listOfTesters = []
counterOfTester = 0
counterOfLogs = 0
listOfPossibleResults = []
testers = driver.find_elements_by_tag_name("a")

for tester in testers:
    tester_name = tester.text
    counterOfTester = counterOfTester + 1
    if counterOfTester > 5:
        listOfTesters.append(tester_name)
        
       
for tester in projectSelected:
    driver.get("http://172.17.70.161/ctplogs/" + tester)
    counterOfLogs = counterOfLogs + 1
    logsResults = driver.find_elements_by_tag_name("a")
        
    for log in logsResults:
        logFile = log.text
        counterOfLogs = counterOfLogs + 1
        if counterOfLogs > 5:
            if serial in logFile:
                result = "http://172.17.70.161/ctplogs/"+ tester + logFile
                listOfPossibleResults.append(result)
                print("..")
                     

print("----------------------------------------------------------------------------------------")
print("Tus Posibles resultados son:")
for result in listOfPossibleResults:
    print (result)
print("----------------------------------------------------------------------------------------")