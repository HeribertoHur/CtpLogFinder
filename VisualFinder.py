from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showwarning
from tkinter.tix import WINDOW
from turtle import width
from selenium import webdriver
from openpyxl import Workbook

PATH = "driver\chromedriver.exe"

#Variables Declaration
listOfTesters = []
listOfPossibleResults = []
justOneTester = ''
window = Tk()
window.title("CTP LOG FINDER")
window.geometry('400x120')

Thor = ["gdlctp7034/","gdlctp7065/", "gdlctp7033/", "gdlctp7053/", "gdlctp7070/", "gdlctp7035/", "gdlctp7036/", "gdlctp7068/"]
CTOATO = ["gdlctp70110/", "gdlctp7027/", "gdlctp7031/", "gdlctp7032/"]
Oracle = ["gdlctp7013/","gdlctp7042/","gdlctp7061/","gdlctp7062/","gdlctp7122/","gdlctp7124/","gdlctp7126/",
          "gdlctp7128/","gdlctp7043/","gdlctp7044/","gdlctp7051/","gdlctp7052/","gdlctp7055/","gdlctp7057/","gdlctp7058/","gdlctp7059/"]
AllTersters = []
for tester in Thor:
    AllTersters.append(tester)
for tester in CTOATO:
    AllTersters.append(tester)
for tester in Oracle:
    AllTersters.append(tester)

def findSerial(SerialNumber, previousTester):
    if previousTester[0] == 'g':
        Logs = getLogs(SerialNumber, previousTester)
    else:
        Logs = getLogs(SerialNumber, getTesters(previousTester))
    createResultSheet(Logs)
    
       
def getInitialMultipleData():
    inputData = ""
    specificNumber = ""
    print("Clearing Content...")
    #TextBox
    inputData = MultipleSerial_entry.get()      #Take the list of seriales
    arrayData = inputData.split(",")            #Split and create an array of seriales
    print("serial numbers ->", arrayData)
    #DropDownSelector
    projectData = clicked.get()
    if projectData == "Project":
        print("A specific Project not was selected...")
    else:
        print("Project Selected ->", projectData)
    #SingleTesterNumber                                        #If the user write the number of just one tester
    specificNumber = "gdlctp"+ specificTester.get() + "/" 
    if specificTester.get() != "":
        print("The specificTester ->", specificNumber)
    else:
        print("A specificTester not was Selected")
    if specificTester.get() != "" and projectData == "Project":
        findSerial(arrayData,specificNumber)
    elif specificTester.get() == "" and projectData != "Project":
        findSerial(arrayData,projectData)
    elif specificTester.get() != "" and projectData != "Project":
        messagebox.showinfo('information', 'Ingrese solo una opción entre un tester Especifico o proyecto')
    #---------------------------------------------------------------------------------------------------------------------
    
def getTesters(project):            #From the buttonSelector get the project
    projectSelected = ""
    if project == "Thor":           #Once selected the variable projectSelected, get the list of thesters of each project
        projectSelected = Thor
    elif project == "CTOATO":
        projectSelected = CTOATO
    elif project == "Oracle":
        projectSelected = Oracle
    elif project == "Proyecto":
        projectSelected = Oracle
    elif project == "TODOS":
        projectSelected = AllTersters
            
    return projectSelected

def getLogs(Seriales, testers):
    if testers[0]=='g':
        justOneTester = testers
        counterOfLogs = 0
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(PATH,options=option)
        driver.get("http://172.17.70.161/ctplogs/" + justOneTester)
        logsResults = driver.find_elements_by_tag_name("a")
        for log in logsResults:
                logFile = log.text
                counterOfLogs = counterOfLogs + 1
                if counterOfLogs > 5:
                    for serial in Seriales:
                        if serial in logFile:                                         # Compare, if the text of the tag "a" contains the serial number
                            result = "http://172.17.70.161/ctplogs/"+ justOneTester + logFile #Gonna save the Link with the tester and the name 
                            listOfPossibleResults.append(result)                       # Inside of a list  
                            print(result,"Was ADDED to the list of possibilites")  
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(PATH,options=option)
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
                            print(result,"Was ADDED to the list of possibilites")
                            
    return listOfPossibleResults
     
# SERIAL EXAMPLE:  SGFGD2214654524             
def createResultSheet(resultLogs):
    print("Creating a File...")
    if resultLogs != []:
        wb = Workbook()
        ws = wb.active
        ws.title = "Examples"
        for log in resultLogs:
            ws.append([log])
        wb.save("LogFiles" + '.xlsx')
        messagebox.showinfo('information', 'Se ha creado un documento con los logs obtenidos!')
        print("Exiting...")
    else:
        messagebox.showwarning('warning', 'No se encontro ningun resultado')
    print("Exiting...")
    
#DropDown Project Selector
clicked = StringVar()
clicked.set("Project")
dropSelector = OptionMenu(window, clicked,"Project", "Thor", "CTOATO","Oracle","TODOS")
dropSelector.pack(pady=5)
dropSelector.place(x=10, y=10)

# specific tester fields
label2 = Label(window,text="Ingresa un solo tester (XXXX):")
label2.pack()
label2.place(x=10, y=50)
specificTester = Entry(window, width=15)
specificTester.get()
specificTester.pack()
specificTester.place(x=180, y=50)

label = Label(window,text="Ingresa serial(es):")
label.pack()
label.place(x=10, y=80)

#InputFieldWithMultipleOption
MultipleSerial_entry = Entry(window, width=43)
MultipleSerial_entry.get()
MultipleSerial_entry.pack(pady=5)
MultipleSerial_entry.place(x=120, y=80)
boton = Button(window, text="Find Serial",pady=5,command=getInitialMultipleData)
boton.pack()
boton.place(x=320, y=10)


window.mainloop()

