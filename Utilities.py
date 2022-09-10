# input is the full distribution, remove all the numbers [ids] from the participants names
import PySimpleGUI as sg
import Constants


def POP_UP(msg):
    sg.popup(msg, title="Error Occured", keep_on_top=True)
    return
    
def removeNumbersFromNamesOfParticipants(distribution):
    for day in distribution:
        for activity in day.keys():
            for participant in day[activity]:
                participant.name = clearNumbersFromString(participant.name)


def clearNumbersFromString(string):
    cleanString = ""
    for letter in string:
        if not letter.isnumeric():
            cleanString = cleanString + letter
    return cleanString

def CumulutiveCapacitySanityCheck(numParticipants,activities):
    cumulutiveCapacities = 0
    for act in activities:
        cumulutiveCapacities += int(act.capacity)
    
    if numParticipants>cumulutiveCapacities:
        POP_UP("שגיאה- יש יותר משתתפים ממקומות בסדנאות")
        raise False
        