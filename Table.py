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

    def addToPot(self, amount):
        self.pot += amount
    
    # doubles both bet amount and raise amount
    def doubleAmounts(self):
        self.raiseAmount = self.raiseAmount * 2
        self.betAmount = self.betAmount * 2 

    def bettingRound(self, state, counter):
        if len(self.activeAgents) <= 1:
            return False

        if counter == 0:
            self.betAmount = self.bigBlind

        nAgents = len(self.activeAgents)
        while nAgents > 0:
            self.passTurn()    
            msg = self.sendMessage(self.turn, [state, self.betAmount, self.raiseAmount])
            #msg = self.receiveMessage(self.turn)
            if "RAISE" in msg:
                self.betAmount += self.raiseAmount
                self.addToPot(self.betAmount)
            elif "CALL" in msg:
                self.addToPot(self.betAmount)
            elif "FOLD" in msg:
                self.activeAgents.pop(self.turn)
            nAgents -= 1
        
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

    def sendMessage(self, agent, msg):
        return self.activeAgents[agent].receiveMessage(msg)
    
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

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)
        
        # pre flop: betting round
        if not self.bettingRound("PRE-FLOP", 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return

        ################ FLOP PHASE ################
        # discard card
        self.discardCard()

        # flop: place 3 cards showing on table
        self.dealCardsTable(3)

        # flop: betting round
        if not self.bettingRound("FLOP", 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return

        ################ TURN PHASE ################
        # turn: double bet ammount and raise ammount
        self.doubleAmounts()

        # turn: add 1 card showing on table
        self.dealCardsTable(1)

        # turn: betting round
        if not self.bettingRound("TURN", 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return

        ################ RIVER PHASE ################
        # river: double bet ammount and raise ammount
        self.doubleAmounts()

        # river: add 1 card showing on table
        self.dealCardsTable(1)

        # river: betting round
        if not self.bettingRound("RIVER", 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return

        ################ SHOWDOWN PHASE ################
        
        best = []
        cardRank = 0
        for a in self.activeAgents:
            if cardRank < a.showHand():
                cardRank = a.showHand()
                best.clear()
                best.append(a)
            elif cardRank == a.showHand():
                best.append(a)
        
        for a in best:
            a.receivePot(self.pot/len(best))

        return
    
    
    def game(self, rounds):
        r = 0
        while r < rounds:
            if len(self.agents) <= 1:
                break
            self.gameRound()
            for a in self.agents:
                if a.getMoney() == 0:
                    self.agents.pop(a)
            self.reset(self.bigBlind)
            r += 1


line = sys.stdin.readline()
numRounds = int(line.split(' ')[0])
numAgents = int(line.split(' ')[1])
bigBlind = int(line.split(' ')[2])
table = Table(numRounds, numAgents, bigBlind)
table.game(numRounds)
