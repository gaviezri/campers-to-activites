# from argparse import Action
from networkx.algorithms.flow import edmonds_karp
import BinDivider, Activity
import networkx as nx
import Constants
import Utilities
from random import shuffle
import UserInterface as ui


class MinFlowParing:

    # generate the graph using the bin (list of participants) and the activities, build the graph such that from
    # stating node s goes an edge to each participant, From each participant to each of its chosen activities
    # and from each activity to the target node t
    def generateGraph(bin, activities):
        graph = nx.DiGraph()
        # s = source , t= target, demand flow of the exact number of participants in a bin (so all participants will
        # get paired), s has negative flow because it should "give" that amount of flow
        graph.add_node(Constants.SOURCE_NODE, demand=-len(bin), weight=1)
        graph.add_node(Constants.TARGET_NODE, demand=len(bin), weight=1)
        # add participants nodes by name
        for participant in bin:
            graph.add_node(participant.name, obj=participant)
        # add the activity names as nodes
        graph.add_nodes_from([act.name for act in activities])

        # add the edges from s to all the kids and from all the kids to their chosen activities
        for participant in bin:
            # add edge from each to every participant
            graph.add_edge(Constants.SOURCE_NODE, participant.name, capacity=1, weight=1)
            # add an edge for each activity chosen from the participant to that activity
            for actName in participant.preferences.keys():
                # add an edge only if the counter is greater than one
                if participant.preferences[actName] > 0:
                    graph.add_edge(participant.name, actName, capacity=1, weight=1)

        # add the edges from all the activities to t
        for act in activities:
            graph.add_edge(act.name, Constants.TARGET_NODE, capacity=int(act.capacity))

        return graph

    # return Distribution which is a dictionary of day which values are dictionaries of activities
    # which values are kids paired to the activity
    # @participants - list of participants
    # @activities - list containing each activity and its capacity
    # @days - number of days for distributing
    def distribution(participants, activities, days):
        fullDistribution = []
        for day in range(days):
            # copy activities
            # shuffle the participants list
            # shuffle(participants)
            currentActivities = activities.copy()
            # generate the current graph based on the bin and activities given
            dataGraph = MinFlowParing.generateGraph(participants, currentActivities)
            try:
                # use the min_cost_flow algorithm to for paring
                minFlowGraphResult = nx.min_cost_flow(dataGraph).copy()
            except:
                msg = "סדנאות שהגיעו ל-0 הם כאלה שיש יותר מידי ילדים שביקשו אותם"
                activityCap = MinFlowParing.getMinFlowGraphExceptionList(participants, minFlowGraphResult, activities)
                Utilities.POP_UP(f"{activityCap} \n- {msg}")
                return None
            # append the current day distribution as a list to the Distribution list
            currentDayDistribution = MinFlowParing.minFlowGraphToPartiActivityList(participants, minFlowGraphResult,
                                                                                   activities)
            fullDistribution.append(currentDayDistribution)
            MinFlowParing.updateParticipantsCapacities(participants, minFlowGraphResult, activities)
            dataGraph.clear()
        return fullDistribution

    # parse the minFlowGraph into a dictionary
    def minFlowGraphToPartiActivityList(participants, minFlowGraph, activities):
        activityWithParticipantsDict = {}
        # generate the list of participants for each activity
        for activity in activities:
            activityWithParticipantsDict[activity.name] = []
        for participant in participants:
            for activity in activities:
                # check if the activity is a choice for the participant
                if activity.name in minFlowGraph[participant.name]:
                    # this activity was chosen for the participant
                    if minFlowGraph[participant.name][activity.name] == 1:
                        activityWithParticipantsDict[activity.name].append(participant)

        return activityWithParticipantsDict

    # update the participants capacities for each of their activities so it wont be picked again (decrease the counter of the chosen activity by one)
    def updateParticipantsCapacities(participants, minFlowGraph, activities):
        # participant.preferences[actName] = participant.preferences[actName] - 1
        for participant in participants:
            for activity in activities:
                # check if the activity is a choice for the participant
                if activity.name in minFlowGraph[participant.name]:
                    # this activity was chosen for the participant
                    if minFlowGraph[participant.name][activity.name] == 1:
                        participant.preferences[activity.name] = participant.preferences[activity.name] - 1

    # check the if any maximum capacity is being exeeced after an exception
    def getMinFlowGraphExceptionList(participants, minFlowGraphResult, activities):
        activitiesCopy = activities.copy()
        for participant in participants:
            for activity in activitiesCopy:
                # check if the activity is a choice for the participant
                if activity.name in minFlowGraphResult[participant.name]:
                    # this activity was chosen for the participant
                    if minFlowGraphResult[participant.name][activity.name] == 1:
                        activity.capacity = str(int(activity.capacity) - 1)
        activitiesPlacesLeft = dict()
        for activity in activitiesCopy:
            activitiesPlacesLeft[activity.name] = f"places left = {activity.capacity}"
        return activitiesPlacesLeft

    def __init__(self, bins, activities, days):
        return
