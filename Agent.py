from enum import Enum
from queue import Queue
from Chips import Chips
from Deck import Deck
from MCTS import MCTS
from Node import StepNode
import utils
import random
import itertools

class Action(Enum):
    #NONE = "none"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    FOLD = "fold"
    #SHOWHAND = "show hand"
    #PAYBLIND = "pay blind"



class Agent:
    #desire = Desire.CALL
    action = None
    #plan = Queue().queue 

    def __init__(self, identifier, table):
        self.table = table
        self.id = identifier
        self.money = Chips(5000)
        self.hand = []
        self.handVal = 0
        self.cardHistory = []
        self.deck = Deck()
        self.currentBetAmount = 0
        self.currentRaiseAmount = 0
        self.state = None
        self.roundHistory = []
        self.roundAverage = 0
        #self.tree_policy = tree_policy
        #self.default_policy = default_policy
        #self.backup = backup
    
    def getId(self):
        return self.id
    
#################################################
####            DECISION-MAKING             #####
#################################################

#    def Monte_Carlo_Search(self):
#        mcts = MCTS(self.tree_policy, self.default_policy, self.backup)
#
#        root = Node(None, self.ownDeck, self.hand, self.tableGetState())
#        root.n += 1
#        root.sample_state()
#
#        action = mcts(root, self.ownDeck, self.hand)
    
    def randomChoice(self, canCheck, canRaise):
        actions = list(Action)
        if not canCheck:
            del actions[2]
        if not canRaise:
            del actions[1]
        self.action = random.choice(actions)
        return self.action

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

    def receiveMessage(self, msg):
        self.state = msg[0]
        self.currentBetAmount = msg[1]
        self.currentRaiseAmount = msg[2]
        canCheck = msg[3]
        canRaise = msg[4]
        return [self.makeBet(self.currentBetAmount, self.currentRaiseAmount, canCheck, canRaise), self.id]

    def sendMessage(self,msg):
        return [msg, self.id]

        #sendMessage(Chips, "Fold")
        #sendMessage(Card)
        #sendMessage(2 Cards)

        #receiveMessage(Chips, "Fold")
        #receiveMessage(Card)
        #receiveMessage(2 Cards)
    
    def receiveCards(self, cardList):
        for card in cardList:
            self.cardHistory.append(card)
            self.deck.removeCard(card.getName())

    def showHand(self):
        self.findHand()
        return self.handVal
    def receivePot(self, potAmount):
        self.money.collect(potAmount)

#################################################
####            AUXILIARY?               ########
#################################################
    
    def calculateRoundAverage(self, counter):
        self.roundHistory.append(counter)
        self.roundAverage = sum(self.roundHistory)/len(self.roundHistory)
    
    def getRoundBet(self):
        return self.money.getRoundBet()

    def resetRoundBet(self):
        self.money.resetRoundBet()

    def getMoney(self):
        return self.money.getCurrent()
    
    def payBlind(self, amount):
        self.money.bet(amount)
        self.resetRoundBet()
    
    def makeBet(self, betAmount, raiseAmount, canCheck, canRaise):
        #action = self.randomChoice(canCheck, canRaise)

        if self.state != "PRE-FLOP":
            level = 0
            if self.state == "TURN": level = 1
            if self.state == "RIVER": level = 2 
            tree = MCTS()
            root = StepNode(None, level, None, len(self.table.activeAgents), self.table.gameState, self.deck, self.cardHistory, self.handVal, self.roundAverage, 
                        self.table.pot, self.money.getGameBet(), self.currentBetAmount, self.currentRaiseAmount)
            for _ in range(2):
                tree.rollout(root)
            #print("------------------------------------------------ROLLOUT DONE-------------------------------------------")
            #print(self.table.gameState)
            #print(root.isTerminal())
            action = tree.choose(root, canCheck, canRaise)

            if action.creationAction == "CALL":
                self.money.bet(betAmount)
                return "CALL"
            elif action.creationAction == "RAISE":
                self.money.bet(betAmount + raiseAmount)
                return "RAISE"
            elif action.creationAction == "FOLD":
                return "FOLD"
            elif action.creationAction == "CHECK":
                return "CHECK"
        else:
            self.money.bet(betAmount)
            return "CALL"

    def reset(self):
        self.hand = []
        self.cardHistory = []
        self.deck = Deck()

#################################################
####            AUXILIARY               #########
#################################################

    def returnRank(self, card):
        return card.getNumericalValue()

    def findHand(self, returnRating = False):
        possible_hands = itertools.combinations(self.cardHistory, 5)
        rating = 0
        best = None
        for hand in possible_hands:
            current = self.rateHand(list(hand))
            if current > rating:
                rating = current
                best = hand
        self.hand = best
        self.handVal = rating
        if returnRating:
            return rating

    def rateHand(self, hand):
        opt1 = self.checkRanks(hand)
        opt2 = self.checkSequence(hand)
        opt3 = self.checkSuits(hand)
        
        #if its a high card
        if opt1 == None and opt2 == None and opt3 == None:
            temp = hand
            temp.sort(key=self.returnRank)
            return temp[-1].getNumericalValue() - 1
        #if its a pair/two pairs/three of a kind/four of a kind/full house
        if opt1 != None and opt2 == None and opt3 == None:
            return opt1
        #if its a straight
        if opt1 == None and opt2 != None and opt3 == None:
            return 52 + (opt2.getNumericalValue()-2)
        #if its just a flush 
        if opt1 == None and opt2 == None and opt3 != None:
            return 62 + (opt3.getNumericalValue()-2)
        #if its a flush and repeated cards see which one is higher
        if opt1 != None and opt2 == None and opt3 != None:
            if opt1 > 62 + (opt3.getNumericalValue()-2):
                return opt1
            else:
                return 62 + (opt3.getNumericalValue()-2)
        #if its a flush and a sequence
        if opt1 == None and opt2 != None and opt3 != None:
            #if its a royal flush
            if opt2.getNumericalValue() == 10:
                return 110
            #if its a straight flush
            else:
                return 101 + (opt2.getNumericalValue()-2)
    
    def checkRanks(self, hand):
        repeats = []
        times = []
        for card in hand:
            if card.getNumericalValue() in repeats:
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
            if 3 in times:
                return 40 + (repeats[times.index(3)]-2)
            #two pair
            else:
                firstRank = repeats[times.index(2)]
                index = times.index(2)
                times.pop(index)
                secondRank = repeats[times.index(2)]
                if firstRank > secondRank:
                    return 27 + (firstRank -2)
                else:
                    return 27 + (secondRank -2)
        if len(repeats) == 2:
            #four of a kind
            if 4 in times:
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
            temp.sort(key=self.returnRank)
            return temp[-1]
    
    def checkSequence(self, hand):
        temp = hand
        temp.sort(key=self.returnRank)
        i = 0
        seq = True
        while i < len(temp)-1:
            if temp[i].getNumericalValue()+1 != temp[i+1].getNumericalValue():
                seq = False
                break
            else:
                i += 1
        if not seq:
            return None
        else:
            return temp[0]


#################################################
####            SENSORS                     #####
#################################################

#    def checkMyCards(self):
#        return self.cards
#
#    def checkMyDeck(self):
#        return self.deck
#
#    def checkTableCards():
#        return table.cards
#    
#    def checkTurn():
#        return table.turn
#    
#    def checkMyChips(self):
#        return self.money.getCurrent()
#    
#    def checkTheirChips(self):
#        chips = []
#        for agent in table.agents:
#            chips.add(agent.cards)
#        return chips
#    
#    def checkPot():
#        return table.pot
#
#    def checkBlind():
#        return table.blind
#
#    def checkPlayRecords():
#        pass
#
#    def checkProfiles():
#        pass
#
#    def checkEnvironment():
#        pass
