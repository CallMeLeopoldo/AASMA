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


    def bettingRound(self, state, counter):

        if counter == 0:
            self.betAmount = self.bigBlind

        nAgents = len(self.activeAgents)
        toRemove = []
        while nAgents > 0:
            self.passTurn() 
            msg = self.sendMessage(self.turn, [state, self.betAmount, self.raiseAmount])
            #msg = self.receiveMessage(self.turn)
            if "RAISE" == msg[0]:
                self.betAmount += self.raiseAmount
                self.addToPot(self.betAmount)
            elif "CALL" == msg[0]:
                self.addToPot(self.betAmount)
            elif "FOLD" == msg[0]:
                toRemove.append(self.activeAgents[self.turn])
            nAgents -= 1
        
        for el in toRemove:
            self.activeAgents.remove(el)

        bet = 0
        newRound = False
        for a in self.activeAgents:
            if bet == 0:
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
                return True

    
    def reset(self, bigBlind):
        self.deck = Deck()
        self.pot = 0
        self.tableCards = []
        self.gameState = None
        self.raiseAmmount = bigBlind
        self.betAmmount = bigBlind
        self.currentBet = 0

        self.dealer += 1

        self.activeAgents.clear()
        for a in self.agents:
            a.reset()
            self.activeAgents.append(a)

    
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
        #print("------------PRE-GAME PHASE------------")
        self.turn = self.dealer

        # pay small blind and big blind
        self.blinds()

        self.deck.shuffle()

        # deal 2 cards to each agent
        for a in self.agents:
            self.dealCardsAgent(a)
        
        #print("------------PRE-FLOP PHASE------------")
        # pre flop: betting round
        if not self.bettingRound("PRE-FLOP", 0):
            if len(self.activeAgents) == 1:
                self.activeAgents[0].receivePot(self.pot)
            return

        ################ FLOP PHASE ################
        #print("------------FLOP PHASE------------")
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
        #print("------------TURN PHASE------------")
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
        #print("------------RIVER PHASE------------")
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
        #print("##################### STARTING THE GAME #####################")
        r = 0
        while r < rounds:
            #print("################### ROUND NO." + str(r+1) + " ###################")
            if len(self.agents) <= 1:
                break
            self.gameRound()
            #msg = ""
            for a in self.agents:
                if a.getMoney() == 0:
                    self.agents.pop(a)
            #    else:
            #        msg = msg + str(a.id) + "; "
            #print("Agents currently playing: " + msg)
            self.reset(self.bigBlind)
            #print("Reseting conditions")
            r += 1


line = sys.stdin.readline()
numRounds = int(line.split(' ')[0])
numAgents = int(line.split(' ')[1])
bigBlind = int(line.split(' ')[2])
table = Table(numRounds, numAgents, bigBlind)
table.game(numRounds)
