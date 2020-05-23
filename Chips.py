##########################################################################
# Chips are the currency of the game.
# This class is initialized with an initial value and keeps track of
# how the game evolves for the agent. The agent can refer back to this
# class to see how much it has lost or gained through the game
##########################################################################

class Chips:

    def __init__(self, value):
        self.initial = value
        self.current = value
        self.gameBet = 0
        self.roundBet = 0
        self.lost = 0
        self.gained = 0

    ##################################################
    ####                 GETTERS                 #####
    ##################################################

    def getInitial(self):
        return self.initial
    
    def getCurrent(self):
        return self.current

    def getGameBet(self):
        return self.gameBet
    
    def getRoundBet(self):
        return self.roundBet

    def getLost(self):
        return self.lost

    def getGained(self):
        return self.gained

    def resetRoundBet(self):
        self.roundBet = 0
        
    ##################################################
    ####              GAME ACTIONS               #####
    ##################################################
    
    def bet(self, blind):
        self.gameBet += blind
        self.roundBet += blind
        self.current -= blind

    def fold(self):
        self.lost += self.gameBet
        self.roundBet = 0
        self.gameBet = 0

    def collect(self, pot):
        self.current += pot
        self.gained += pot
        self.roundBet = 0
        self.gameBet = 0