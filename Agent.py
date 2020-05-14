from enum import Enum
from queue import Queue
from Chips import Chips
import utils
import random

class Desire(Enum):
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    FOLD = "fold"

class Action(Enum):
    NONE = "none"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    FOLD = "fold"
    SHOWHAND = "show hand"
    PAYBLIND = "pay blind"



class Agent:
    desire = Desire.CALL
    action = Action.NONE
    plan = Queue.queue 

    def __init__(self, identifier):
        self.id = identifier
        self.money = Chips(5000)
        self.hand = []
    
#################################################
####            DECISION-MAKING             #####
#################################################


#################################################
####         REACTIVE BEHAVIOUR             #####
#################################################

    def agentReactiveDecision(self):
        pass

#################################################
####            COMMUNICATION               #####
#################################################

    def updateBeliefs(self):
        pass

    def sendMessage(self):
        table.sendMessage()

        #sendMessage(Chips, "Fold")
        #sendMessage(Card)
        #sendMessage(2 Cards)

        #receiveMessage(Chips, "Fold")
        #receiveMessage(Card)
        #receiveMessage(2 Cards)

#################################################
####            AUXILIARY               #########
#################################################

    def buildPathPlan():
        pass

#################################################
####            SENSORS                     #####
#################################################

    def checkMyCards(self):
        return self.cards

    def checkTableCards():
        return table.cards
    
    def checkTurn():
        return table.turn
    
    def checkMyChips(self):
        return self.money.getCurrent()
    
    def checkTheirChips(self):
        chips = []
        for agent in table.agents:
            chips.add(agent.cards)
        return chips
    
    def checkPot():
        return table.pot

    def checkBlind():
        return table.blind

    def checkPlayRecords():
        pass

    def checkProfiles():
        pass

    def checkEnvironment():
        pass
