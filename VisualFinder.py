from tkinter import *
from selenium import webdriver
from openpyxl import Workbook
from datetime import date

PATH = "C:\Driver\chromedriver.exe"

#Variables Declaration
listOfTesters = []
listOfPossibleResults = []

window = Tk()
window.title("CTP LOG FINDER")
window.geometry('400x150')
window.iconbitmap('find.ico')

Thor = ["gdlctp7034/","gdlctp7065/", "gdlctp7033/", "gdlctp7053/", "gdlctp7070/", "gdlctp7035/", "gdlctp7036/", "gdlctp7068/" ]
CTOATO = ["gdlctp70110/", "gdlctp7027/", "gdlctp7031/", "gdlctp7032/"]
Oracle = ["gdlctp7013/","gdlctp7042/","gdlctp7061/","gdlctp7062/","gdlctp7122/","gdlctp7124/","gdlctp7126/",
          "gdlctp7128/","gdlctp7043/","gdlctp7044/","gdlctp7051/","gdlctp7052/","gdlctp7055/","gdlctp7057/","gdlctp7058/","gdlctp7059/"]


def findSerial(SerialNumber, project):
    print(SerialNumber, project)
    Logs = getLogs(SerialNumber, getTesters(project))
    createResultSheet(Logs)
        
def getInitialMultipleData():
    #TextBox
    inputData = MultipleSerial_entry.get()
    #DropDownSelector
    projectData = clicked.get()
    arrayData = inputData.split(",")
    findSerial(arrayData,projectData)
    
def getTesters(project):
    projectSelected = ""
    if project == "Thor":
        projectSelected = Thor
    elif project == "CTOATO":
        projectSelected = CTOATO
    elif project == "Oracle":
            projectSelected = Oracle
            
    return projectSelected

def getLogs(Seriales, testers):
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
                for serial in Seriales:
                    if serial in logFile:                                         # Compare, if the text of the tag "a" contains the serial number
                        result = "http://172.17.70.161/ctplogs/"+ tester + logFile #Gonna save the Link with the tester and the name 
                        listOfPossibleResults.append(result)                       # Inside of a list
    return listOfPossibleResults
     
# SERIAL EXAMPLE:  SGFGD2214654524             
def createResultSheet(resultLogs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Examples"
    for log in resultLogs:
        ws.append([log])
    wb.save("ejemplo" + '.xlsx')
    
#DropDown Project Selector
clicked = StringVar()
clicked.set("Project")
dropSelector = OptionMenu(window, clicked, "Thor", "CTOATO","Oracle")
dropSelector.pack()

#InputFieldWithMultipleOption
MultipleSerial_entry = Entry(window)
MultipleSerial_entry = Text(height=3,width=40)
MultipleSerial_entry.pack(pady=5)
Button(window, text="Find Serial",pady=5,height=1, width=30,command=getInitialMultipleData).pack()

window.mainloop()