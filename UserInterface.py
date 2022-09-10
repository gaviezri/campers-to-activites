from Activity import Activity
import Constants
import PySimpleGUI as sg
import Parser
import Utilities





def UserChoice():
    while (StartSorting()):

        DataHandler = Choose_File_Parse_File()
        if DataHandler == 'Back':
            continue
        activitySet = createActivities(DataHandler[Constants.ACTIVITY_NAME_FROM_EXCEL_KEY])
        if activitySet == False:
            continue
        if DataHandler != None:
            return activitySet, DataHandler
        if DataHandler == False:
            raise False
    return None, None


# starting window of the application returns the participants list
def StartSorting():
    sg.theme('BlueMono')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('\nKimama', auto_size_text=True)],
              [sg.Button('Start')], [sg.Button('Exit')]
              ]

    # Create the Window
    window = sg.Window('Sort Campers To Activities', layout, element_justification='c',
                       size=(320, 120), icon='Kimama-icon.ico')
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(close=True)
        # TODO: [KIM-10] add flow for when file that chose was not in format OR no file was chosen
        if event == 'Start':
            return True
        if event == 'Exit' or event == sg.WIN_CLOSED:
            raise False

def createActivities(activitiesNames):
    layout = [setActivityInputLines(activitiesNames)]

    window = sg.Window('Sort Campers To Activities', layout,size=(420,220),
                       element_justification='l',icon='Kimama-icon.ico')
    

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            raise False
        if event == 'Continue':
            window.close()
            return createActivitiyList(values, activitiesNames)
        if event == 'Back':
            window.close()
            return False


# generate set of activity objects (name,capacity) based on user's input
def createActivitiyList(values, activitiesName):
    ActivityList = []
    # iterate over i=(0,len), actName = current Activity in set
    for i, actName in zip(range(len(activitiesName)), activitiesName):
        if values['Cap' + str(i)].isdigit() == False or values['Cap' + str(i)] == '':
            # throw exception and message for user if capacity is not an integer
            Utilities.POP_UP("capacity can contain only Numbers!")
            raise False
        ActivityList.append(Activity(values['Cap' + str(i)], actName))
    return ActivityList


# create input line for GUI that gets capacity for each activity
def setActivityInputLines(activities):
    activityInp = [[sg.Text("Please enter maximum participants per acitvity:")]]

    for i, activity in zip(range(len(activities)), activities):
        # add a line with input for capacity
        activityInp.append([sg.Input("Capacity", key='Cap' + str(i)), sg.Text(activity)])

    activityInp.append([sg.Button("Continue"), sg.Button("Back")])
    return activityInp


def Choose_File_Parse_File():
    layout = [
        [sg.Text("Choose Excel File: ")],
        [sg.FileBrowse(initial_folder=Constants.DESKTOP, key="CHOSEN-FILE"), sg.Input(key="FILE-PATH")],
        [sg.Button('Sort Campers', disabled=True, key="BEGIN-SORT"), sg.Button('Back')]
    ]
    # Create the Window
    window = sg.Window('Sort Campers To Activities', layout, size=(420, 120), icon='Kimama-icon.ico')
    # Event Loop to process "events" and get the "values" of the inputs
    timeout = 100
    while True:
        event, values = window.Read(timeout)
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            window.close()
            raise False
        if event == 'Back':
            window.close()
            return 'Back'

        if event == "BEGIN-SORT":
            window.close()
            if values["CHOSEN-FILE"][-1:-5:-1]!='xslx' and values["CHOSEN-FILE"][-1:-4:-1]!='csv':
                Utilities.POP_UP("wrong file format (only xlsx or csv)")
                raise False
            DataDict = Parser.parseExcelFileToDict(values["CHOSEN-FILE"])
            return DataDict

        if values["CHOSEN-FILE"] != '':
            window["BEGIN-SORT"].update(disabled=False)
            timeout = Constants.ONE_MINUTE
            window.refresh()
