import sys
from Deck import Deck
from Agent import Agent

class Table:
    
    def __init__(self, numRounds, numAgents, bigBlind):
        self.numRounds = numRounds
        self.agents = []
        self.activeAgents = []
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.discardPile = []
        self.gameState = None

        self.bigBlind = bigBlind
        self.smallBlind = round(bigBlind/2)
        self.raiseAmount = bigBlind
        self.betAmount = bigBlind
        self.currentBet = 0

        self.dealer = 0
        self.turn = 0

        i = 0
        while i < numAgents:
            agent = Agent(i)
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

    # agents pay small blind and big blind 
    def blinds(self):
        self.passTurn()
        self.agents[self.turn].payBlind(self.smallBlind)
        self.passTurn()
        self.agents[self.turn].payBlind(self.bigBlind)

    # self.turn has the activeAgents index. returns agent id
    def passTurn(self):
        nextTurn = self.turn
        if nextTurn > len(self.activeAgents)-1:
            nextTurn = 0
        self.turn = nextTurn

    # discards one card
    def discardCard(self):
        card = self.deck.dealCard()
        self.discardPile.append(card)
        
    # places one card on the table
    def dealCardsTable(self, num):
        n = 0
        while n < num: 
            card = self.deck.dealCard()
            self.tableCards.append(card)
            n += 1

    # deals two cards to agent
    def dealCardsAgent(self, agent):
        card1 = self.deck.dealCard()
        card2 = self.deck.dealCard()
        agent.receiveCards(card1, card2)

    def addToPot(self, amount):
        self.pot += amount
    
    # doubles both bet amount and raise amount
    def doubleAmounts(self):
        self.raiseAmount = self.raiseAmount * 2
        self.betAmount = self.betAmount * 2 

    # TODO: this will be the full betting round
    def bettingRound(self, state, counter):
        if len(self.activeAgents) <= 1:
            return False

        if counter == 0:
            self.betAmount = self.bigBlind

        nAgents = len(self.activeAgents)
        while nAgents > 0:
            self.passTurn()    
            self.sendMessage(self.turn, [state, self.betAmount, self.raiseAmount])
            msg = self.receiveMessage(self.turn)
            if "RAISE" in msg:
                self.betAmount += self.raiseAmount
                self.pot += self.betAmount
            elif "CALL" in msg:
                self.pot += self.betAmount
            elif "FOLD" in msg:
                self.activeAgents.pop(self.turn)
        
        bet = 0
        newRound = False
        for a in self.activeAgents:
            if bet == 0:
                bet = a.getRoundBet()
            elif a.getRoundBet() != bet:
                newRound = True
                break

        if counter == 4:
            return True

        if (newRound):
            counter += 1
            self.bettingRound(state, counter)


        

        #move dealer button to next player
        #send state to agents ?
        #for a in agents: a.decide ?
        #add chips to pot
        #update agents still playing
        #if agents 
    
    def reset(self, bigBlind):
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.gameState = None
        self.raiseAmmount = bigBlind
        self.betAmmount = bigBlind
        self.currentBet = 0

        self.dealer += 1

        for a in self.agents:
            a.reset()

    
    #################################################
    ####            COMMUNICATION               #####
    #################################################

    # TODO
    def sendMessage(self, agent, msg):
        pass
    
    # TODO
    def receiveMessage(self, agent):
        pass

    #################################################
    ####                  GAME                  #####
    #################################################
    
    def gameRound(self):
        
        self.turn = self.dealer

        # pay small blind and big blind
        self.blinds()

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)
        
        # pre flop: betting round
        self.bettingRound("PRE-FLOP", 0)

        # discard card
        self.discardCard()

        # flop: place 3 cards showing on table
        self.dealCardsTable(3)

        # flop: betting round
        self.bettingRound("FLOP", 0)

        # turn: double bet ammount and raise ammount
        self.doubleAmmounts()

        # turn: add 1 card showing on table
        self.dealCardsTable(1)

        # turn: betting round
        self.bettingRound("TURN", 0)

        # river: double bet ammount and raise ammount
        self.doubleAmmounts()

        # river: add 1 card showing on table
        self.dealCardsTable(1)

        # river: betting round
        self.bettingRound("RIVER", 0)

        # showdown
        #check if there is more than one active player
        #check who is the winner
        #attribute pot? idk is this would even make sense bc the game is over and the agents would stop existing now
    
    
    def game(self, rounds):
        r = 0
        while r < rounds:
            if len(self.agents) <= 1:
                break
            self.gameRound()
            self.reset(self.bigBlind)
            r += 1


line = sys.stdin.readline()
numRounds = line.split(' ')[0]
numAgents = line.split(' ')[1]
bigBlind = line.split(' ')[2]
table = Table(numRounds, numAgents, bigBlind)
table.game(numRounds)
