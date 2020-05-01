from enum import Enum
from queue import Queue

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

    def __init__(self,):
        this.money = 5000
    
#################################################
####            DECISION-MAKING             #####
#################################################

    def agentDecision(self):
        updateBeliefs()
        if not plan.isEmpty() and (not succeededIntention()) and  not (impossibleIntention()):
            Action action = plan.remove()
            if(isPlanSound(action)):
                execute(action) 
            else:
                rebuildPlan()
            if reconsider():
                deliberate()
                
            else:
                deliberate()
                buildPlan()
                if(plan.isEmpty()):
                    agentReactiveDecision()
    
    def deliberate(self):
        pass

    def buildPlan(self):
        pass

    def rebuildPlan(self):
        pass
    
    def isPlanSound(self):
        pass

    def execute(self):
        pass
    def impossibleIntention(self):
        pass
    def succeededIntention(self):
        pass
    def reconsider(self):
        pass


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

#################################################
####            AUXILIARY               #########
#################################################

    def buildPathPlan():
        pass

#################################################
####            SENSORS               #####
#################################################

    def checkMyCards():
        pass

    def checkTableCards():
        pass
    
    def checkTurn():
        pass
    
    def checkMyChips():
        pass    

    def checkTheirChips():
        pass
    
    def checkPot():
        pass

    def checkBlind():
        pass

    def checkPlayRecords():
        pass

    def checkProfiles():
        pass

    def checkEnvironment():
        pass

    