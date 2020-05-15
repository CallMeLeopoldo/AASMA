from enum import Enum
from queue import Queue
from Chips import Chips
from MCTS import MCTS
import utils
import random
import itertools

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

    def __init__(self, identifier, tree_policy, default_policy, backup):
        self.id = identifier
        self.money = Chips(5000)
        self.hand = []
        self.ownDeck = []
        self.tree_policy = tree_policy
        self.default_policy = default_policy
        self.backup = backup
    
#################################################
####            DECISION-MAKING             #####
#################################################

    def decisionMaking(self):
        mcts = MCTS(self.tree_policy, self.default_policy, self.backup)

        root = Node(None, self.ownDeck, self.hand, self.tableGetState())
        root.n += 1
        root.sample_state()

        action = mcts(root, self.ownDeck, self.hand)

#################################################
####         REACTIVE BEHAVIOUR             #####
#################################################

    def agentReactiveDecision(self):
        pass

#################################################
####            COMMUNICATION               #####
#################################################

    def tableGetState(self):
        pass
        #communicate w table to get which state the game is in, i.e flop, turn, river, etc
    
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

    def findHand():
        possible_hands = itertools(self.hand, 5)
        rating = 0
        best = None
        for hand in possible_hands:
            curent = rateHand(hand)
            if current > rating:
                rating = current
                best = hand
        self.hand = best
    
    def rateHand(hand):
        pass
        #basically check all possible combinations of agents cards and cards on table to find the hand currently held. will have to implement this in Node as well


#################################################
####            SENSORS                     #####
#################################################

    def checkMyCards(self):
        return self.cards

    def checkMyDeck(self):
        return self.deck

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
