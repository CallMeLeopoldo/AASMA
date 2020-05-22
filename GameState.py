class GameState:

    def __init__(self):
        self.betAmount = 0
        self.raiseAmount = 0
        self.state = None
        #self.roundHistory = []
        #self.roundAverage = 0
        #self.playRecord = []
        self.canCheck = True
        self.canRaise = False
        self.possibleActions = []
    
    # ------- getters ---------- 

    def getBetAmount(self):
        return self.betAmount
    
    def getRaiseAmount(self):
        return self.raiseAmount
    
    def getSate(self):
        return self.state
    
    #def getRoundHistory(self):
    #    return self.roundHistory
    #
    #def getRoundAverage(self):
    #    return self.roundAverage
    
    #def getFullPlayRecord(self):
    #    return self.fullPlayRecord

    def getCanCheck(self):
        return self.canCheck

    def getCanRaise(self):
        return self.canRaise
    
    def getActions(self):
        return self.possibleActions
    
    # ------ setters -------
    
    def setBetAmount(self, amount):
        self.betAmount = amount
    
    def setRaiseAmount(self, amount):
        self.raiseAmount = amount
    
    def setState(self, state):
        self.state = state

    #def setRoundHistory(self, hist):
    #    self.roundHistory = hist

    #def setRoundAverage(self, avg):
    #    self.roundAverage = avg
    
    def setCanCheck(self, boolean):
        self.canCheck = boolean
    
    def setCanRaise(self, boolean):
        self.canRaise = boolean
    
    def setActions(self, actions):
        self.possibleActions = actions

    # -----------------

    #def incrementRoundHistory(self, n):
    #    self.roundHistory.append(n)
    #
    #def calculateRoundAverage(self):
    #    self.roundAverage = sum(self.roundHistory)/len(self.roundHistory)

    # -----------------

    def updateGameState(self, other):
        self.setBetAmount(other.getBetAmount())
        self.setRaiseAmount(other.getRaiseAmount())
        self.setState(other.getSate())
        #self.setRoundHistory(other.getRoundHistory())
        #self.setRoundAverage(other.getRoundAverage())
        self.setCanCheck(other.getCanCheck())
        self.setCanRaise(other.getCanRaise())
        self.setActions(other.getActions())
