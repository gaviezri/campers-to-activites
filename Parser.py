from csv import excel
from ctypes import util
from datetime import date, datetime
from heapq import merge
from numpy import datetime_as_string
import pandas as pd
from Participant import Participant
import Constants
import xlsxwriter as XL
import UserInterface as ui
import Utilities


def GetNumberOfDays(excel_data):
    excelKeys = []
    numberOfDays = 0
    for j in excel_data:
        # check if a key is a course and increase the days counter ( number of columns of courses = number of days)
        if Constants.EXCEL_COL_ACTIVITY in j:
            numberOfDays += 1
    return numberOfDays


def GetParticipantsList_GetActivityNames(excel_data):
    activityNames = set()
    participantList = []
    id = 0
    for row in range(len(excel_data)):
        # current participant
        participant = Participant(None, None, None, None)
        # current participant activities
        participantActivities = {}
        # go through each key for each row in the excel table
        for key in excel_data:
            currentKeyValue = str(excel_data.loc[row].get(key))
            # check if a key is a spe0cific attribute then add accordingly
            # key is the name col
            if Constants.EXCEL_COL_NAME in key:
                participantName = f"{currentKeyValue}{id}"
                participant.name = participantName
                id = id + 1
            # key is the grade col
            if Constants.EXCEL_COL_GRADE in key:
                participant.grade = currentKeyValue
            # key is one of the activities col ( aka courses)
            if Constants.EXCEL_COL_ACTIVITY in key:
                insertActivityToDict(participantActivities, currentKeyValue)
                # add the activity to the activitySet
                activityNames.add(currentKeyValue)
            # key is the medical problems
            if Constants.EXCEL_COL_MEDICAL_PROBLEMS in key:
                if currentKeyValue == 'nan':
                    participant.medical_cond = Constants.EXCEL_MEDIAL_PROBLEM_DEFAULT_VALUE
                else:
                    participant.medical_cond = currentKeyValue

        # now add all the choruses to the participant attribute
        participant.preferences = participantActivities
        # all the attributes are filled, add to the participantsList
        participantList.append(participant)
        if participant.name == None and row == 0:
            Utilities.POP_UP("No participants detected in file")
            raise False

    return participantList, activityNames


def parseExcelFileToDict(filePath):
    # Load the xlsx file
    excel_data = pd.read_excel(filePath)
    # get all the keys (columns) of the excel table??? NEEDED???
    # get number of days
    numberOfDays = GetNumberOfDays(excel_data)

    participantsList, activityNames = GetParticipantsList_GetActivityNames(excel_data)

    # return the participant list
    return {Constants.PARTICIPANTS_KEY: participantsList,
            Constants.DAYS_OF_ACTIVITIES_KEY: numberOfDays,
            Constants.ACTIVITY_NAME_FROM_EXCEL_KEY: activityNames}


# add the activity name to the list, if exists only incrase the counter otherwise add it
def insertActivityToDict(dictOfActivities, activitiyName):
    if activitiyName in dictOfActivities:
        dictOfActivities[activitiyName] = dictOfActivities[activitiyName] + 1
    else:
        dictOfActivities[activitiyName] = 1


# TODO finish this function

def parseDictToExcelFile(distribution, activities):
    Filename = 'Kimama Kids in Activities ' + datetime.now().strftime("%m-%d-%y") + '.xlsx'
    Fullpath = Constants.DESKTOP + '\\' + Filename
    # per sheet
    # iterate over the first row, merge every 3 cells with 1 cell space and text 'activity'
    # iterate over the second row, 'name' 'grade' 'medical'
    # insert particiapnts name = x.name yada...
    try:

        with XL.Workbook(Fullpath) as workbook:
            format = merge_format_creator(workbook)
            for Nday in range(1, len(activities) + 1):
                worksheet = workbook.add_worksheet('Day ' + str(Nday))
                insertDataToSheet(distribution[Nday - 1], worksheet, insertSheetHeaders(worksheet, activities, format),
                                  activities, workbook)
        return True
    except:
        return False


def insertDataToSheet(ActivityParticipantsDict, sheet, activity_idx, activities, workbook):
    for act in activities:
        Entryrow = 0
        ActivityParticipantsDict[act.name].sort(key=lambda x: x.grade)
        while (Entryrow < len(ActivityParticipantsDict[act.name])):
            insertParticipantEntry(sheet, Entryrow + 2, activity_idx[act.name],
                                   ActivityParticipantsDict[act.name][Entryrow], workbook)
            Entryrow += 1

    return


def insertParticipantEntry(sheet, row, col, participant, workbook):
    # format of the participant entry
    cell_format = workbook.add_format({'align': 'center'})
    # set the name column width to be 3 cells long
    sheet.set_column(row, col, 15)
    # add the entry
    sheet.write(row, col, participant.medical_cond, cell_format)
    sheet.write(row, col + 1, participant.grade, cell_format)
    sheet.write(row, col + 2, participant.name, cell_format)


def merge_format_creator(WB):
    return WB.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#D7E4BC',
    })


def insertSheetHeaders(worksheet, activities, format):
    activity_idx_dict = {}
    for act, col in zip(activities, range(0, len(activities) * 4, 4)):
        activity_idx_dict[act.name] = col
        worksheet.merge_range(0, col, 0, col + 2, act.name, format)
        worksheet.write(1, col, 'רפואי')
        worksheet.write(1, col + 1, 'כיתה')
        worksheet.write(1, col + 2, 'שם')
    return activity_idx_dict
