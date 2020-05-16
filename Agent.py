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

    def Monte_Carlo_Search(self):
        mcts = MCTS(self.tree_policy, self.default_policy, self.backup)

        root = Node(None, self.ownDeck, self.hand, self.tableGetState())
        root.n += 1
        root.sample_state()

        action = mcts(root, self.ownDeck, self.hand)
    
    def randomChoice(self):
        return action

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

    def findHand(self):
        possible_hands = itertools(self.hand, 5)
        rating = 0
        best = None
        for hand in possible_hands:
            curent = rateHand(hand)
            if current > rating:
                rating = current
                best = hand
        self.hand = best
    
    def rateHand(self, hand):
        opt1 = self.checkRanks(hand)
        #if it has more than one card of the same rank its not a sequence or a flush
        if opt1 != None:
            return opt1
        opt2 = self.checkSequence(hand)
        opt3 = self.checkSuits(hand)
        #if its a high card
        if opt2 == None and opt3 == None:
            temp = hand
            temp.sort()
            return temp[-1] - 1
        #if its a flush
        if opt2 == None and opt3 != None:
            return 62 + (opt3-2)
        #if its a straight
        if opt2 != None and opt3 == None:
            return 52 + (opt2-2)
        if opt2 != None and opt3 != None:
            #if its a royal flush
            if opt2 = 10 and hand[0].getSuit() == "Spades":
                return 110
            #if its a straight flush
            else:
                return 101 + (opt2-2)
    
    def checkRanks(self, hand):
        repeats = []
        times = []
        for card in hand:
            if card.getValue() in repeats:
                times[repeats.index(card.getNumericalValue())] += 1
            else:
                repeats.append(card.getNumericalValue())
                times.append(1)
        if len(repeats) == 5:
            return None
        #pair
        if len(repeats) == 4:
            return 14 + (repeats[times.index(2)]-2)
        if len(repeats) == 3:
            #three of a kind
            if 3 in repeats:
                return 40 + (repeats[times.index(3)]-2)
            #two pair
            else:
                firstRank = repeats[times.index(2)]
                times.pop(firstRank)
                secondRank = repeats[times.index(2)]
                if firstRank > secondRank:
                    return 27 + (firstRank -2)
                else:
                    return 27 + (secondRank -2)
        if len(repeats) == 2:
            #four of a kind
             if 4 in repeats:
                return 88 + (repeats[times.index(4)]-2)
            #full house
            else:
                return 75 + (repeats[times.index(3)]-2)

    def checkSuits(self, hand):
        #clubs diamonds hearts spades
        suits = [0, 0, 0, 0]
        for card in hand:
            if card.getSuit() == "Clubs":
                suits[0] += 1
            elif card.getSuit() == "Diamonds":
                suits[1] += 1
            elif card.getSuit() == "Hearts":
                suits[2] += 1
            elif card.getSuit() == "Spades":
                suits[3] += 1
        if 5 not in suits:
            return None
        else:
            temp = hand
            temp.sort()
            return temp[-1]
    
    def checkSequence(self, hand):
        temp = hand
        temp.sort()
        i = 0:
        seq = True
        while i < len(temp):
            if temp[i] != (temp[i+1] + 1):
                seq = False
                break
            else:
                i += 1
        if !seq:
            return None
        else:
            return temp[0]


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
