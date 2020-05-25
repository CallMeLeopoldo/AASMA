##########################################################################
# Gamestate controls the state of the game in Table and with the Agents.
# This class optimizes updates in the state of the game and their
# communication among the various entities of the game.
##########################################################################

class GameState:

    def __init__(self):
        self.betAmount = 0
        self.raiseAmount = 0
        self.state = None
        self.canCheck = True
        self.canRaise = False
        self.possibleActions = []
    
    ##################################################
    ####                 GETTERS                 #####
    ##################################################

    def getBetAmount(self):
        return self.betAmount
    
    def getRaiseAmount(self):
        return self.raiseAmount
    
    def getSate(self):
        return self.state

    def getCanCheck(self):
        return self.canCheck

    def getCanRaise(self):
        return self.canRaise
    
    def getActions(self):
        return self.possibleActions
    
    ##################################################
    ####                 SETTERS                 #####
    ##################################################
    
    def setBetAmount(self, amount):
        self.betAmount = amount
    
    def setRaiseAmount(self, amount):
        self.raiseAmount = amount
    
    def setState(self, state):
        self.state = state
    
    def setCanCheck(self, boolean):
        self.canCheck = boolean
    
    def setCanRaise(self, boolean):
        self.canRaise = boolean
    
    def setActions(self, actions):
        self.possibleActions = actions

    ##################################################
    ####                 UPDATE                  #####
    ##################################################

    def updateGameState(self, other):
        self.setBetAmount(other.getBetAmount())
        self.setRaiseAmount(other.getRaiseAmount())
        self.setState(other.getSate())
        self.setCanCheck(other.getCanCheck())
        self.setCanRaise(other.getCanRaise())
        self.setActions(other.getActions())
