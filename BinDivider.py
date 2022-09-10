import Constants


"""
BinDivider divides the list of participants into a number of bins
"""
class BinDivider:
    """
    get the bins filled with participants
    The algorithm first picks the rightmost and leftmost bins and start by adding the highest grades to one bin and
    the lowest grades to the other bin, we will fill each bin until it is full [bin-limit] and when it is we will move
    onto the next bin - the number of bins are chosen dynamically from the Constants file
    """

    def getBinsOfParticipants(participants):
        # The number of participants allowed per bin (rough limit not tight boundary)
        binLimit = len(participants) // Constants.NUMBER_OF_BINS
        # create the number of bins dynamically
        bins = [[] for b in range(Constants.NUMBER_OF_BINS)]
        # first and last students in the list
        lowParticipantIndex = 0
        highParticipantIndex = len(participants) - 1
        # the previous lowest/highest grades, if current grade is different then previous then we can check of conds
        previousLowestGrade = participants[0].grade
        previousHighestGrade = participants[len(participants) - 1].grade
        # index for the current bins that are being filled
        lowerBinIndex = 0
        highestBinIndex = len(bins) - 1
        # start adding the students from edges, finish when all the students were added
        while lowParticipantIndex <= highParticipantIndex:
            # if indexes are equal its the last person to add to a bin
            if lowParticipantIndex == highParticipantIndex:
                if previousLowestGrade == participants[lowParticipantIndex].grade:
                    bins[lowerBinIndex].append(participants[lowParticipantIndex])
                else:
                    bins[highestBinIndex].append(participants[highestBinIndex])
                break
            # firstly add the lowest grades to the lower bin
            # if the current participant is in the same grade as the preciousLowestGrade
            if participants[lowParticipantIndex].grade == previousLowestGrade:
                bins[lowerBinIndex].append(participants[lowParticipantIndex])
                lowParticipantIndex += 1
            # the bin limit has not been reached
            elif len(bins[lowerBinIndex]) <= binLimit:
                bins[lowerBinIndex].append(participants[lowParticipantIndex])
                lowParticipantIndex += 1
            else:
                # in this case we the bin is already full and also the new participants is not in same grade as others
                previousLowestGrade = participants[lowParticipantIndex].grade
                lowerBinIndex += 1
                # add participant to next bin
                bins[lowerBinIndex].append(participants[lowParticipantIndex])
                # increase counter of index only after appending
                lowParticipantIndex += 1

            # secondly add the highest grades to the highest been
            # if the current participant is in the same grade as previous then add him to bin
            if participants[highParticipantIndex] == previousHighestGrade:
                bins[highestBinIndex].append(participants[highParticipantIndex])
                highParticipantIndex -= 1
            # the bin limit has not been reached
            elif len(bins[highestBinIndex]) <= binLimit:
                bins[highestBinIndex].append(participants[highParticipantIndex])
                highParticipantIndex -= 1
            # the bin is full and the new participant is in another grade, add him to the next bin
            else:
                previousHighestGrade = participants[highParticipantIndex].grade
                highestBinIndex -= 1
                # add the participant to the new bin index
                bins[highestBinIndex].append(participants[highestBinIndex])
                highParticipantIndex -= 1

        return bins
