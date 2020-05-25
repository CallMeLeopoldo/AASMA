##########################################################################
# Table is our Game Manager and runs the game.
# Table keeps a lot of information in state. It controls the game, 
# creates Agents and checks which ones are active in game round or in
# game.
# This file also contains the functions that permit the reading
# of input through the command line. Do not delete
# The prints in this file allow us to view the proceedings of the game.
# To watch risk calculation activate the prints indicated in class Agent.
##########################################################################

import sys
import ratings
import keyboard
from Deck import Deck
from Agent import Agent
from GameState import GameState

class Table:
    
    def __init__(self, numRounds, numAgents, bigBlind, chips, agentProfiles = None):
        self.numRounds = numRounds
        self.agents = []
        self.activeAgents = []
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.discardPile = []

        self.gameStateClass = GameState()
        self.gameState = None

        self.bigBlind = bigBlind
        self.smallBlind = round(bigBlind/2)
        self.raiseAmount = bigBlind
        self.betAmount = bigBlind
        self.currentBet = 0

        self.canCheck = True
        self.canRaise = False

        self.dealer = 0
        self.turn = 0

        self.agentProfiles = agentProfiles

        i = 0
        while i < numAgents:
            if agentProfiles == None:
                agent = Agent(i, self, chips)
            else:
                agent = Agent(i, self, chips, agentProfiles[i])
            self.agents.append(agent)
            self.activeAgents.append(agent)
            i += 1


    ##################################################
    ####                 GETTERS                 #####
    ##################################################

    def getAgents(self):
        return self.agents
    
    def getDeck(self):
        return self.deck
    
    def getPot(self):
        return self.pot

    ##################################################
    ####             DEALER ACTIONS              #####
    ##################################################

    def addToPot(self, amount):
        self.pot += amount

    # agents pay small blind and big blind 
    def blinds(self):
        self.passTurn()
        self.agents[self.turn].payBlind(self.smallBlind)
        print("AGENT " + str(self.turn) + " PAYED SMALL BLIND: " + str(self.smallBlind))
        self.addToPot(self.smallBlind)
        self.passTurn()
        self.agents[self.turn].payBlind(self.bigBlind)
        print("AGENT " + str(self.turn) + " PAYED BIG BLIND: " + str(self.bigBlind))
        self.addToPot(self.bigBlind)

    # self.turn has the activeAgents index. returns agent id
    def passTurn(self):
        nextTurn = self.turn
        if nextTurn >= len(self.activeAgents)-1:
            nextTurn = 0
        else:
            nextTurn += 1
        self.turn = nextTurn

    # discards one card
    def discardCard(self):
        card = self.deck.dealCard()
        self.discardPile.append(card)

    # places one card on the table
    def dealCardsTable(self, num):
        n = 0
        dealtCards = []
        while n < num: 
            card = self.deck.dealCard()
            self.tableCards.append(card)
            dealtCards.append(card)
            n += 1
        for a in self.activeAgents:
            a.receiveCards(dealtCards)

    # deals two cards to agent
    def dealCardsAgent(self, agent):
        card1 = self.deck.dealCard()
        card2 = self.deck.dealCard()
        agent.receiveCards([card1, card2])

    # doubles both bet amount and raise amount
    def doubleAmounts(self):
        self.raiseAmount = self.raiseAmount * 2
        self.betAmount = self.betAmount * 2 

    def whatToDo(self):
        actions = ["CALL","FOLD"]
        if self.canCheck:
            actions.append("CHECK")
        if self.canRaise:
            actions.append("RAISE")
        return actions

    def bettingRound(self, state, counter):
        #which actions are allowed at beginning of a betting round
        if counter == 0:
            self.betAmount = self.bigBlind
            self.canCheck = True
            self.canRaise = False

        nAgents = len(self.activeAgents)
        toRemove = []

        while nAgents > 0:
        
            self.passTurn()
            actions = self.whatToDo()

            self.updateGameState(state, actions)

            msg = self.sendMessage(self.turn)
            
            if(len(toRemove) == len(self.activeAgents) - 1):
                break
            if "RAISE" == msg[0]:
                self.betAmount += self.raiseAmount
                self.addToPot(self.betAmount)
                self.canCheck = False
                print("AGENT " + str(msg[1]) + " DID " + msg[0] + " AND BET " + str(self.betAmount))
            elif "CALL" == msg[0]:
                self.addToPot(self.betAmount)
                self.canCheck = False
                self.canRaise = True
                print("AGENT " + str(msg[1]) + " DID " + msg[0] + " AND BET " + str(self.betAmount))
            elif "FOLD" == msg[0]:
                self.activeAgents[self.turn].fold()
                toRemove.append(self.activeAgents[self.turn])
                print("AGENT " + str(msg[1]) + " DID " + msg[0] + " AND IS REMOVED FROM GAME ROUND")
            elif "CHECK" == msg[0]:
                print("AGENT " + str(msg[1]) + " DID " + msg[0] + " AND DID NOT BET")
            
            if self.activeAgents[self.turn].getMoney() <= 0:
                toRemove.append(self.activeAgents[self.turn])
                print("AGENT " + str(msg[1]) + " RAN OUT OF MONEY AND IS REMOVED FROM GAME")
            
            print("POT CURRENTLY AT " + str(self.pot))

            #WARN OTHER AGENTS
            self.sendWarn("warn", [self.turn, msg[0]])

            nAgents -= 1
                    
        #removes agents who have folded
        for el in toRemove:
            self.activeAgents.remove(el)

        #to guarantee agents have bet the same
        bet = -1
        newRound = False
        for a in self.activeAgents:
            if bet == -1:
                bet = a.getRoundBet()
            elif a.getRoundBet() != bet:
                newRound = True
                break

        if newRound and counter < 3:
            counter += 1
            return self.bettingRound(state, counter)
        else:
            if len(self.activeAgents) <= 1:
                return False
            else:
                for a in self.activeAgents:
                    a.resetRoundBet()
                    a.calculateRoundAverage(counter+1)
                return True
    
    #reset table structures for another gameround
    def reset(self, bigBlind):
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.gameState = None
        self.raiseAmount = bigBlind
        self.betAmount = bigBlind
        self.currentBet = 0

        self.dealer += 1

        self.activeAgents.clear()
        for a in self.agents:
            a.reset()
            self.activeAgents.append(a)

    
    #################################################
    ####            COMMUNICATION               #####
    #################################################

    def updateGameState(self, state, actions):
        self.gameStateClass.setBetAmount(self.betAmount)
        self.gameStateClass.setRaiseAmount(self.raiseAmount)
        self.gameStateClass.setState(state)
        self.gameStateClass.setCanCheck(self.canCheck)
        self.gameStateClass.setCanRaise(self.canRaise)
        self.gameStateClass.setActions(actions)

    def sendMessage(self, agent):
        self.activeAgents[agent].updateGameState(self.gameStateClass)
        return self.activeAgents[agent].receiveMessage()

    def sendWarn(self, flag, msg):
        for a in self.activeAgents:
            if(a.id != self.turn):
                a.receiveWarn(flag,msg)

    #################################################
    ####                  GAME                  #####
    #################################################
    
    def gameRound(self):
        
        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        
        ################ PRE GAME PHASE ################
        self.turn = self.dealer

        # pay small blind and big blind
        self.blinds()

        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        self.deck.shuffle()

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)

        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("\nCARDS ARE DEALT TO THE AGENTS")

        #EVALUATE STATE OF GAME
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id))
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())
        
        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        
        ################ PRE FLOP PHASE ################
        print("\n----- PRE-FLOP -----")
        self.gameState = "PRE-FLOP"

        print("\nBETTING STARTS")

        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        # pre flop: betting round
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id) + " RECEIVES: " + str(self.pot) + "\n")
            return

        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
            
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + "; PROFILE " + a.getProfile() + "; MONEY: " + str(a.money.getCurrent()) + "; TOTAL BET:" + str(a.money.getGameBet()))

        for a in self.activeAgents:
            if a.getMoney() <= 0:
                self.activeAgents.remove(a)
        
        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        ################ FLOP PHASE ################
        print("\n----- FLOP -----")
        self.gameState = "FLOP"

        # discard card
        self.discardCard()

        # flop: place 3 cards showing on table
        self.dealCardsTable(3)

        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
            
        #print(self.gameState)
        print("\nCARDS ARE DEALT TO THE TABLE: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        
        print("\nPLAYERS HOLD:")
        for a in self.activeAgents:
            print("->AGENT " + str(a.id) + " HAS: " + str(ratings.handName[a.showHand()]))
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())
            print("Press 1 to continue")
            while(True):
                b = keyboard.read_key()
                if b == "1":
                    break
        
        # flop: betting round
        print("\nBETTING STARTS")
        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id) + " RECEIVES: " + str(self.pot) + "\n")
            return
        
        print("\nBETTING ENDS")

        print("Press 1 to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        print("STATE OF THE AGENTS AFTER THE FLOP BETTING ROUND")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + "; PROFILE " + a.getProfile() + "; MONEY: " + str(a.money.getCurrent()) + "; TOTAL BET:" + str(a.money.getGameBet()))
        
        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)

        ################ TURN PHASE ################
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        print("\n----- TURN -----")
        self.gameState = "TURN"

        # turn: double bet ammount and raise ammount
        self.doubleAmounts()

        # turn: add 1 card showing on table
        self.dealCardsTable(1)
        
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        
        print("\nPLAYERS HOLD:")
        for a in self.activeAgents:
            print("Press to continue")
            while(True):
                b = keyboard.read_key()
                if b == '1':
                    break
            print("->AGENT " + str(a.id) + " HAS: " + str(ratings.handName[a.showHand()]))
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())

        # turn: betting round
        print("\nBETTING STARTS")
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id) + " RECEIVES: " + str(self.pot) + "\n")
            return
        
        print("\nBETTING ENDS")
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        print("STATE OF THE AGENTS AFTER THE TURN BETTING ROUND")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + "; PROFILE " + a.getProfile() + "; MONEY: " + str(a.money.getCurrent()) + "; TOTAL FAR: " + str(a.money.getGameBet()))

        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)

        ################ RIVER PHASE ################
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("\n----- RIVER -----")
        self.gameState = "RIVER"

        # river: double bet ammount and raise ammount
        self.doubleAmounts()

        # river: add 1 card showing on table
        self.dealCardsTable(1)
        
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        
        print("\nPLAYERS HOLD:")
        for a in self.activeAgents:
            print("Press to continue")
            while(True):
                b = keyboard.read_key()
                if b == '1':
                    break
            print("->AGENT " + str(a.id) + " HAS: " + str(ratings.handName[a.showHand()]))
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())
            
        # river: betting round
        print("\nBETTING STARTS")
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id) + " RECEIVES: " + str(self.pot) + "\n")
            return

        print("\nBETTING ENDS")
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("STATE OF THE AGENTS AFTER THE RIVER BETTING ROUND")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + "; PROFILE " + a.getProfile() + "; MONEY: " + str(a.money.getCurrent()) + "; TOTAL FAR: " + str(a.money.getGameBet()))
        
        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)

        ################ SHOWDOWN PHASE ################
        self.gameState = "SHOWDOWN"
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("\n----- SHOWDOWN -----")

        best = []
        cardRank = 0
        
        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())

        print("Press to continue")
        while(True):
            a = keyboard.read_key()
            if a == '1':
                break

        print("\nPLAYERS HOLD:")
        for a in self.activeAgents:
            print("Press to continue")
            while(True):
                b = keyboard.read_key()
                if b == '1':
                    break
            print("->AGENT " + str(a.id) + " HAS: " + str(ratings.handName[a.showHand()]))
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())


        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + "; PROFILE: " + a.getProfile() + "; MONEY: " + str(a.money.getCurrent()) + "; TOTAL BET: " + str(a.money.getGameBet()))
        
        for a in self.activeAgents:
                if a.money.getCurrent() <= 0:
                    self.activeAgents.remove(a)

        for a in self.activeAgents:
            if cardRank < a.findHand(True):
                cardRank = a.findHand(True)
                best.clear()
                best.append(a)
            elif cardRank == a.findHand(True):
                best.append(a)
        
        for a in best:
            a.receivePot(self.pot/len(best))
            print("WINNING AGENT: " + str(a.id) + " RECEIVES: " + str(self.pot) + "\n")

        return
    
  
    def game(self, rounds):
        print("##################### GAME BEGINS #####################")
        r = 0
        while r < rounds:
            
            if len(self.agents) <= 1:
                break
            
            print("============= GAME ROUND " + str(r+1) + " =============")
            self.gameRound()
            
            for a in self.agents:
                if a.getMoney() <= 0:
                    self.agents.pop(self.agents.index(a))
            
            self.reset(self.bigBlind)
            
            r += 1
        print("##################### GAME ENDS #####################")


line = sys.stdin.readline()
numRounds = int(line.split(' ')[0])
numAgents = int(line.split(' ')[1])
bigBlind = int(line.split(' ')[2])
chips = int(line.split(' ')[3])
if len(line.split(' ')) == 4:
    table = Table(numRounds, numAgents, bigBlind, chips)
    table.game(numRounds)
else:
    i = 0
    profiles = []
    while i < numAgents:
        profiles.append(int(line.split(" ")[3].split(",")[i]))
        i += 1
    print(profiles)
    if len(profiles) != numAgents:
        print("Wrong number of agent profiles")
    else:
        table = Table(numRounds, numAgents, bigBlind, chips, profiles)
        table.game(numRounds)
