import UserInterface as ui
import Constants
import MinFlowParing
import Parser
import Utilities


# mainWindow sole purpose is to return the participant array
def main():
    try:
        activities, kimamaDataset = ui.UserChoice()
        Utilities.CumulutiveCapacitySanityCheck(len(kimamaDataset.get(Constants.PARTICIPANTS_KEY)), activities)
    except:
        return Constants.FAILED_TO_EXECUTE

    if kimamaDataset is None or activities is None:
        Utilities.POP_UP("KimamaDataset / activities are None - אנא סגור ונסה שנית")
        return Constants.FAILED_TO_EXECUTE
    else:
        # get all the data needed to run the the Min-Flow algorithm and sorting to bins
        participants = kimamaDataset.get(Constants.PARTICIPANTS_KEY)
        numberOfDays = kimamaDataset.get(Constants.DAYS_OF_ACTIVITIES_KEY)
        # sort the participants into bins
        # bins = BinDivider.BinDivider.getBinsOfParticipants(participants)
        # run the MinFlow algorithm and inside output the excel files TODO: catch any erros in case minFlow did not work
        distribution = MinFlowParing.MinFlowParing.distribution(participants, activities, numberOfDays)

        if distribution is None:
            Utilities.POP_UP("distribution is None - אנא צא ונסה שנית")
            return Constants.FAILED_TO_EXECUTE
        # clean up the numbers in participants names
        Utilities.removeNumbersFromNamesOfParticipants(distribution)
        # parse the distribution for each day to an excel file
        result = Parser.parseDictToExcelFile(distribution, activities)
        if result is False:
            Utilities.POP_UP("שגיאה ביצירת קובץ הפלט")

        Utilities.POP_UP("קובץ נוצר בהצלחה")
        return Constants.EXECUTED_SUCCESSFULY


if __name__ == "__main__":
    main()
