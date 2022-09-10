import os

EXCEL_COL_NAME = "שם"
EXCEL_COL_GRADE = "כיתה"
EXCEL_COL_ACTIVITY = "סדנה"
EXCEL_COL_MEDICAL_PROBLEMS = "רפואי"

EXCEL_MEDIAL_PROBLEM_DEFAULT_VALUE = "אין"

# the keys for the excel table
ACTIVITY_KEY = "activties"
ACTIVITY_NAME_FROM_EXCEL_KEY = "activity_names"
PARTICIPANTS_KEY = "participants"
DAYS_OF_ACTIVITIES_KEY = "number_of_days"

# TODO check if needs
GRADES_KEY = "grades"

# number of bins for participants
NUMBER_OF_BINS = 3

# exitcodes
EXECUTED_SUCCESSFULY = 0
FAILED_TO_EXECUTE = 1

# path constants for filebrowsing
DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
ONE_MINUTE = 60000

# activity dictionary keys for participant
ACTIVITY_NAME_PARTICIPANT = "name"
ACTIVITY_COUNTER_PARTICIPANT = "counter"

# source node and target node of the graph
SOURCE_NODE = "s"
TARGET_NODE = "t"
