from enum import Enum
from queue import Queue
from Chips import Chips
from Deck import Deck
from MCTS import MCTS
from Node import StepNode
from GameState import GameState
import utils
import random
import itertools
import time

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
    action = None   #TODO: check if this should be here 
    #plan = Queue().queue 

    def __init__(self, identifier, table):
        self.table = table
        self.id = identifier
        self.money = Chips(5000)
        self.hand = []
        self.handVal = 0
        self.cardHistory = []
        self.deck = Deck()
        
        #self.currentBetAmount = 0
        #self.currentRaiseAmount = 0
        #self.state = None
        self.roundHistory = []
        self.roundAverage = 0

        self.gameState = GameState()
        
        self.profile = self.setProfile()
        self.playRisk = 0
        self.opponentPlayRecord = []
        #print(self.getProfile())

    
    def getId(self):
        return self.id
    
#################################################
####            DECISION-MAKING             #####
#################################################
    
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

    def agentReactiveDecision(self, actions):

        if(self.getProfile() == "Risky"):
            if(self.risk > 2):
                return "FOLD"
        elif(self.getProfile() == "Safe"):
            if(self.risk > 0.6):
                return "FOLD"
            if(self.risk < 0.3):
                return "CALL"

        elif(self.getProfile() == "HAL-9000"):
            if(self.risk > 0.6):
                return "FOLD"
            if(self.risk < 0.3):
                return "CALL"        

        elif(self.getProfile() == "Dummy"):
            if(self.risk > 1):
                return "FOLD"
            else:
                return random.choice(actions)

        elif(self.getProfile() == "Copycat"):
            if(len(self.checkPlayRecords()) == 0):
                return "CALL"
            return self.checkPlayRecords()[-1]

        return





#################################################
####            COMMUNICATION               #####
#################################################

    def tableGetState(self):
        pass
        #communicate w table to get which state the game is in, i.e flop, turn, river, etc
    
    def updateGameState(self, other):
        self.gameState.updateGameState(other)

    def receiveMessage(self):
        #self.state = msg[0]
        #self.currentBetAmount = msg[1]
        #self.currentRaiseAmount = msg[2]
        #canCheck = msg[3]
        #canRaise = msg[4]
        #actions = msg[5]
        #return [self.makeBet(self.currentBetAmount, self.currentRaiseAmount, canCheck, canRaise, actions), self.id]
        return [self.makeBet(), self.id]

    def receiveWarn(self, flag, msg):
        if(flag == "warn"):
            self.opponentPlayRecord.append(msg[1])
            del self.opponentPlayRecord[ : (-3*len(self.table.agents))]

    def sendMessage(self,msg):
        return [msg, self.id]

    
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
    
    def setProfile(self):
        profile = random.randint(1,5)
        if profile == 1:
            return "Risky"
        elif profile == 2:
            return "Safe"
        elif profile == 3:
            return "Dummy"
        elif profile == 4:
            return "Copycat"
        elif profile == 5:
            return "Balanced"
        return
    
    def calculateRoundAverage(self, counter):
        #self.gameState.incrementRoundHistory(counter)
        #self.gameState.calculateRoundAverage()
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
    
    def riskCalculation(self):
        potF = 0

        #actionF = 0.1*foldF + 0.1*checkF + 0.3*callF + 0.5*raiseF

        moneyF = self.checkTheirChips()/(self.checkTheirChips() + self.checkMyChips())

        if(self.table.pot < 0.25*self.checkMyChips()):
            potF = 0
        elif(self.table.pot < 0.5*self.checkMyChips()):
            potF = 0.25
        elif(self.table.pot < 0.75*self.checkMyChips()):
            potF = 0.5
        elif(self.table.pot < 1*self.checkMyChips()):
            potF = 0.75
        else:
            potF = 1

        self.risk = moneyF*0.5 + potF*0.5
        print(self.risk)

    
    def opponentModelCalculation(self):
        potF = 0
        action = 0
        raiseF = self.opponentPlayRecord.count("RAISE")
        callF = self.opponentPlayRecord.count("CALL")
        foldF = self.opponentPlayRecord.count("FOLD")
        checkF = self.opponentPlayRecord.count("CHECK")

        actionF = 0.1*foldF + 0.1*checkF + 0.3*callF + 0.5*raiseF

        if raiseF != 0:
            raiseF = raiseF/len(self.opponentPlayRecord)

        if callF != 0:
            callF = callF/len(self.opponentPlayRecord)

        if checkF != 0:
            checkF = checkF/len(self.opponentPlayRecord) 

        moneyF = self.checkTheirChips()/(self.checkTheirChips() + self.checkMyChips())

        if(self.table.pot < 0.25*self.checkMyChips()):
            potF = 0
        elif(self.table.pot < 0.5*self.checkMyChips()):
            potF = 0.25
        elif(self.table.pot < 0.75*self.checkMyChips()):
            potF = 0.5
        elif(self.table.pot < 1*self.checkMyChips()):
            potF = 0.75
        else:
            potF = 1

        self.risk = moneyF*0.3 + potF*0.3 + actionF*0.4
        print(self.risk)
        
    
    #def makeBet(self, betAmount, raiseAmount, canCheck, canRaise, actions):
    def makeBet(self):                                                  # TODO fix this
        #action = self.randomChoice(canCheck, canRaise)

        betAmount = self.gameState.getBetAmount()
        raiseAmount = self.gameState.getRaiseAmount()
        canCheck = self.gameState.getCanCheck()
        canRaise = self.gameState.getCanRaise()
        actions = self.gameState.getActions()
        state = self.gameState.getSate()
        #roundAvg = self.gameState.getRoundAverage()
        roundAvg = self.roundAverage

        self.riskCalculation()

        if state != "PRE-FLOP":
            level = 0
            if state == "TURN": level = 1
            if state == "RIVER": level = 2

            goReactive = self.agentReactiveDecision(actions)
            if(goReactive is not None):
            #RETURN GOREACTIVE
                if goReactive == "CALL":
                    self.money.bet(betAmount)
                    return "CALL"
                elif goReactive == "RAISE":
                    self.money.bet(betAmount + raiseAmount)
                    return "RAISE"
                elif goReactive == "FOLD":
                    return "FOLD"
                elif goReactive == "CHECK":
                    return "CHECK"                
            else:
                tree = MCTS()
                #root = StepNode(None, level, None, len(self.table.activeAgents), self.table.gameState, self.deck, self.cardHistory, self.handVal, self.roundAverage, actions, self.profile,
                #            self.table.pot, self.money.getGameBet(), self.currentBetAmount, self.currentRaiseAmount)
                root = StepNode(None, level, None, len(self.table.activeAgents), state, self.deck, self.cardHistory, self.handVal, roundAvg, actions, self.profile,
                            self.table.pot, self.money.getGameBet(), betAmount, raiseAmount)
                startingTime = time.time()
                for _ in range(100):
                    tree.rollout(root)
                endTime = time.time() - startingTime
                print("THIS IS THE DECISION MAKING-TIMING: " + str(endTime) + " seconds")

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

    def checkMyCards(self):
        return self.hand

    def checkMyDeck(self):
        return self.deck

    def checkTableCards(self):
        return table.tableCards
    
    def checkTurn(self):
        return table.turn
    
    def checkMyChips(self):
        return self.money.getCurrent()
    
    def checkTheirChips(self):
        chips = 0
        for agent in self.table.agents:
            chips += agent.money.getCurrent()
        return chips
    
    def checkPot(self):
        return table.pot

    def checkBlind(self):
        return table.betAmount

    def checkPlayRecords(self):
        return self.opponentPlayRecord

    def getProfile(self):
        return self.profile

    def checkProfiles(self):
        opponentsProfiles = []
        for a in self.table.agents:
            opponentsProfiles.append(a.getProfile())
        return opponentsProfiles

    def checkEnvironment(self):
        return self.table.environment
        pass
