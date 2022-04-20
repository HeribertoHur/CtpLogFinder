from tkinter import *
from selenium import webdriver
from openpyxl import Workbook
from datetime import date


PATH = "C:\Driver\chromedriver.exe"

#Variables Declaration
listOfTesters = []
counterOfTester = 0

listOfPossibleResults = []

window = Tk()
window.title("CTP LOG FINDER")
window.geometry('300x150')

Thor = ["gdlctp7034/","gdlctp7065/", "gdlctp7033/", "gdlctp7053/", "gdlctp7070/", "gdlctp7035/", "gdlctp7036/", "gdlctp7068/" ]
CTOATO = ["gdlctp70110/", "gdlctp7027/", "gdlctp7031/", "gdlctp7032/"]
Oracle = ["gdlctp7013/","gdlctp7042/","gdlctp7061/","gdlctp7062/","gdlctp7122/","gdlctp7124/","gdlctp7126/",
          "gdlctp7128/","gdlctp7043/","gdlctp7044/","gdlctp7051/","gdlctp7052/","gdlctp7055/","gdlctp7057/","gdlctp7058/","gdlctp7059/"]


def findSerial(SerialNumber, project):
    print(SerialNumber, project)
    Logs = getLogs(SerialNumber, getTesters(project))
    createResultSheet(Logs,SerialNumber)
    
 
def getInitialData():
    #TextBox
    inputData = serial_entry.get()
    #DropDownSelector
    projectData = clicked.get()    
    findSerial(inputData,projectData)
    
def getTesters(project):
    projectSelected = ""
    if project == "Thor":
        projectSelected = Thor
    elif project == "CTOATO":
        projectSelected = CTOATO
    elif project == "Oracle":
            projectSelected = Oracle
            
    return projectSelected

def getLogs(Serial, testers):
    driver = webdriver.Chrome(PATH)
    counterOfLogs = 0
    for tester in testers:
        driver.get("http://172.17.70.161/ctplogs/" + tester)    ## We gonna search inside of each tester that the project has
        counterOfLogs = counterOfLogs + 1
        logsResults = driver.find_elements_by_tag_name("a")     # Gonna use the same method, use the tags "a"
        for log in logsResults:
            logFile = log.text
            counterOfLogs = counterOfLogs + 1
            if counterOfLogs > 5:
                if Serial in logFile:                                         # Compare, if the text of the tag "a" contains the serial number
                    result = "http://172.17.70.161/ctplogs/"+ tester + logFile #Gonna save the Link with the tester and the name 
                    listOfPossibleResults.append(result)                       # Inside of a list
        
    return listOfPossibleResults
     
# SERIAL EXAMPLE:  SGFGD2214654524             
def createResultSheet(resultLogs,serial):
    wb = Workbook()
    ws = wb.active
    ws.title = serial
    for log in resultLogs:
        ws.append([log])
    wb.save(serial + '.xlsx')
    
#DropDown Project Selector
clicked = StringVar()
clicked.set("Project")
dropSelector = OptionMenu(window, clicked, "Thor", "CTOATO","Oracle")
dropSelector.pack()

#InputField
serial_entry = Entry(window)
serial_entry.pack(pady=30)
Button(window, text="Find Serial", padx=10, pady=5,command=getInitialData).pack()

window.mainloop()