from Deck import Deck
from Agent import Agent

class Table:
    
    def __init__(self, numAgents, bigBlind):
        self.agents = {}
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.discardPile = []
        self.gameState = None

        self.bigBlind = bigBlind
        self.smallBlind = round(bigBlind/2)
        self.raiseAmmount = bigBlind
        self.betAmmount = bigBlind
        self.currentBet = 0

        id = 0
        while id < numAgents:
            self.agents[id] = Agent(id)
            id += 1



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
        # TODO agent needs to receive cards. if agents has a hand then append to cards to hand?

    def addToPot(self, amount):
        self.pot += amount
    
    # doubles both bet amount and raise ammount
    def doubleAmmounts(self):
        self.raiseAmmount = self.raiseAmmount * 2
        self.betAmmount = self.betAmmount * 2 

    # TODO: this will be the full betting round
    def bettingRound(self):
        pass
        #move dealer button to next player
        #send state to agents ?
        #for a in agents: a.decide ?
        #add chips to pot
        #update agents still playing

    
    #################################################
    ####            COMMUNICATION               #####
    #################################################

    # TODO
    def sendMessage(self, msg, agent):
        pass
    
    # TODO
    def receiveMessage(self, msg, agent):
        pass

    #################################################
    ####                  GAME                  #####
    #################################################
    
    def game(self):
        # attribute button to first player
        self.agents[0].hasButton(True)

        # pay small blind and big blind
        self.agents[1].paySmallBlind()
        self.agents[2].payBigBlind()

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)
        
        # pre flop: betting round
        self.bettingRound()

        #discard card    --- dont remember if its here or not
        self.discardCard()

        # flop: place 3 cards showing on table
        self.dealCardsTable(3)

        # flop: betting round
        self.bettingRound()

        # turn: double bet ammount and raise ammount
        self.doubleAmmounts()       # não tenho a certeza se isto duplica outra vez para o river ou se se mantém

        # turn: add 1 card showing on table
        self.dealCardsTable(1)

        # turn: betting round
        self.bettingRound()

        # river: add 1 card showing on table
        self.dealCardsTable(1)

        # river: betting round
        self.bettingRound()

        # showdown
        #check if there is more than one active player
        #check who is the winner
        #attribute pot? idk is this would even make sense bc the game is over and the agents would stop existing now
        

    # TODO: add hand and dealer button attributes to Agent, add the methods above that refer to agents
