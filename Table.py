import sys
from Deck import Deck
from Agent import Agent
from GameState import GameState

class Table:
    
    def __init__(self, numRounds, numAgents, bigBlind):
        self.numRounds = numRounds
        self.agents = []
        self.activeAgents = []
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.discardPile = []

        self.gameStateClass = GameState()
        self.gameState = None
        #self.environment = environment

        self.bigBlind = bigBlind
        self.smallBlind = round(bigBlind/2)
        self.raiseAmount = bigBlind
        self.betAmount = bigBlind
        self.currentBet = 0

        self.canCheck = True
        self.canRaise = False

        self.dealer = 0
        self.turn = 0

        i = 0
        while i < numAgents:
            agent = Agent(i, self)
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
        self.addToPot(self.smallBlind)
        self.passTurn()
        self.agents[self.turn].payBlind(self.bigBlind)
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

        if counter == 0:
            self.betAmount = self.bigBlind
            self.canCheck = True
            self.canRaise = False

        nAgents = len(self.activeAgents)
        toRemove = []

        while nAgents > 0:
            self.passTurn()
            actions = self.whatToDo()
            #print("VALUE OF CANCHECK: " + str(self.canCheck))
            #print("VALUE OF CANRAISE: " + str(self.canRaise))

            self.updateGameState(state, actions)

            #msg = self.sendMessage(self.turn, [state, self.betAmount, self.raiseAmount, self.canCheck, self.canRaise, actions])
            msg = self.sendMessage(self.turn)
            #msg = self.receiveMessage(self.turn)
            #print("SO THIS IS WHAT THE RETARDED AGENT NUMBER " + str(msg[1]) + " DID " + msg[0])
            #print("AGENT " + str(msg[1]) + " DID " + msg[0])
            if(len(toRemove) == len(self.activeAgents) - 1):
                break
            if "RAISE" == msg[0]:
                #print("WAIT A SECOND")
                self.betAmount += self.raiseAmount
                self.addToPot(self.betAmount)
                self.canCheck = False
            elif "CALL" == msg[0]:
                self.addToPot(self.betAmount)
                self.canCheck = False
                self.canRaise = True
            elif "FOLD" == msg[0]:
                self.activeAgents[self.turn].fold()
                toRemove.append(self.activeAgents[self.turn])
            
            if self.activeAgents[self.turn].getMoney() <= 0:
                toRemove.append(self.activeAgents[self.turn])
            
            print("AGENT " + str(msg[1]) + " DID " + msg[0] + " PUT " + str(self.betAmount)) 
            
            #WARN OTHER AGENTS
            self.sendWarn("warn", [self.turn, msg[0]])

            nAgents -= 1
                    
        for el in toRemove:
            self.activeAgents.remove(el)

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
        #self.gameState.setRoundHistory(other.getRoundHistory())
        #self.gameState.setRoundAverage(other.getRoundAverage())
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
    
    #def receiveMessage(self, agent, msg):
    #    return msg

    #################################################
    ####                  GAME                  #####
    #################################################
    
    def gameRound(self):
        
        ################ PRE GAME PHASE ################
        self.turn = self.dealer

        # pay small blind and big blind
        self.blinds()

        self.deck.shuffle()

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)

        #EVALUATE STATE OF GAME
        print("AGENTS:\n")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE: " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
            print("HAND:")
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())
            print("\n")
        
        ################ PRE FLOP PHASE ################
        print("----- PRE-FLOP -----")
        self.gameState = "PRE-FLOP"

        # pre flop: betting round
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return
        #print(self.gameState)
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
            print("HAND:")
            for c in a.cardHistory:
                print("CARD NUMBER: " + c.getName())

        for a in self.activeAgents:
            if a.getMoney() <= 0:
                self.activeAgents.remove(a)
        ################ FLOP PHASE ################
        print("\n----- FLOP -----")
        self.gameState = "FLOP"

        # discard card
        self.discardCard()

        # flop: place 3 cards showing on table
        self.dealCardsTable(3)

        #print(self.gameState)
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        print("\n")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
    
        # flop: betting round
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("\nWINNING AGENT: " + str(self.activeAgents[0].id) + "\n")
            return
        
        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)
        ################ TURN PHASE ################
        print("\n----- TURN -----")
        self.gameState = "TURN"

        # turn: double bet ammount and raise ammount
        self.doubleAmounts()

        # turn: add 1 card showing on table
        self.dealCardsTable(1)
        #print(self.gameState)
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        print("\n")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
        
        # turn: betting round
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id))
            return
        
        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)
        ################ RIVER PHASE ################
        print("\n----- RIVER -----")
        self.gameState = "RIVER"
        # river: double bet ammount and raise ammount
        self.doubleAmounts()

        # river: add 1 card showing on table
        self.dealCardsTable(1)
        #print(self.gameState)
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        print("\n")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
        
        # river: betting round
        if not self.bettingRound(self.gameState, 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
                print("WINNING AGENT: " + str(self.activeAgents[0].id))
            return
        
        for a in self.activeAgents:
            if a.money.getCurrent() <= 0:
                self.activeAgents.remove(a)
        ################ SHOWDOWN PHASE ################
        self.gameState = "SHOWDOWN"
        print("\n----- SHOWDOWN -----")

        best = []
        cardRank = 0
        #print(self.gameState)
        print("TABLE CARDS: ")
        for c in self.tableCards:
            print("CARD NUMBER: " + c.getName())
        print("\n")
        for a in self.activeAgents:
            print( "AGENT: " + str(a.id) + " PROFILE " + a.getProfile() + " MONEY: " + str(a.money.getCurrent()) + " BET: " + str(a.money.getGameBet()))
        
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
            print("WINNING AGENT: " + str(a.id) + "\n")

        return
    
  
    def game(self, rounds):
        #print("##################### STARTING THE GAME #####################")
        r = 0
        while r < rounds:
            #print("################### ROUND NO." + str(r+1) + " ###################")
            if len(self.agents) <= 1:
                break
            
            print("----- GAME ROUND " + str(r) + " -----")
            self.gameRound()
            #print("we are ending the game at: " + str(self.gameState) + " with " + str(len(self.activeAgents)) + " active agents")
            #msg = ""
            for a in self.agents:
                if a.getMoney() <= 0:
                    self.agents.pop(self.agents.index(a))
            #    else:
            #        msg = msg + str(a.id) + "; "
            #print("Agents currently playing: " + msg)
            self.reset(self.bigBlind)
            #print("Reseting conditions")
            r += 1


line = sys.stdin.readline()
#environment = str(line.split(' ')[0])
numRounds = int(line.split(' ')[0])
numAgents = int(line.split(' ')[1])
bigBlind = int(line.split(' ')[2])
table = Table(numRounds, numAgents, bigBlind)
table.game(numRounds)
