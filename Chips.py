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
        self.bet = 0
        self.lost = 0
        self.gained = 0

    ##################################################
    ####                 GETTERS                 #####
    ##################################################

    def getInitial():
        return self.initial
    
    def getCurrent():
        return self.current

    def getBet():
        return self.bet

    def getLost():
        return self.lost

    def getGained():
        return self.gained
        
    ##################################################
    ####              GAME ACTIONS               #####
    ##################################################
    
    def bet(blind):
        self.bet += blind
        self.current -= blind

    def fold():
        self.lost += self.bet
        self.bet = 0

    def collect(pot):
        self.current += pot
        self.gained += pot
        self.bet = 0