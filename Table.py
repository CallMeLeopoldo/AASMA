from Deck import Deck
from Deck import Card
from Agent import Agent
from Chips import Chips

class Table:
    
    def __init__(self):
        self.agents = {}
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.discardPile = []
        self.gameState = None

        #self.smallBlind
        #self.bigBlind
        #self.raiseAmmount
        #self.currentBet

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
    def dealCardTable(self, agent):
        card = self.deck.dealCard()
        self.tableCards.append(card)

    # deals one card to agent
    def dealCardAgent(self, agent):
        card = self.deck.dealCard()
        # TODO agent needs to receive card. if agents has a hand then append to card to hand?

    def addToPot(self, amount):
        self.pot = self.pot + amount
    
    #################################################
    ####            COMMUNICATION               #####
    #################################################

    def sendMessage(self, msg, agent):
        pass

    def receiveMessage(self, msg, agent):
        pass

    #################################################
    ####                  GAME                  #####
    #################################################