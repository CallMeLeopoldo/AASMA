##########################################################################
# Node is the class that implements the Nodes of the MCTS.
# The subclass StepNode is the one we use here. Each child of the StepNode
# is created through the method sample_state in class Action. This 
# allows for a fluidity in the Nodes that would be impossible otherwise.
##########################################################################

from Deck import Deck
from Deck import Card
import ratings
import random
import copy
import math
import itertools

class Node(object):
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.q = 0
        self.n = 0
        

class Action():
    """
    A node holding an action in the tree.
    """
    def __init__(self, action, node):
        self.action = action
        self.node = node

    def sample_state(self, lst=None):
        if  not self.node.deck.isEmpty():
            
            i = 0
            children = []

            if self.node.level == 2:
                new_level = self.node.level + 1
                temp = "SHOWDOWN"
                child = StepNode(self.node, new_level, self.action, self.node.numPlayers, temp, self.node.deck, self.node.cardHistory, self.node.irlHand, self.node.roundAverage, self.node.actions, self.node.profile, self.node.risk)
                child.currentBetAmount = self.node.currentBetAmount
                child.raiseAmount = self.node.raiseAmount
                child.gameBet = self.node.gameBet
                child.pot = self.node.pot

                if lst == None:
                    children.append(child)
                    return children
                else:
                    lst.append(child)
                    return

            else:
                while i < len(self.node.deck.getCards()):
                    new_card = self.node.deck.getCards()[i]
                    new_deck = copy.deepcopy(self.node.deck)
                    new_deck.removeCard(new_card.getName())
                    new_history = copy.deepcopy(self.node.cardHistory)
                    new_history.append(new_card)

                    if(self.node.level == 0):
                        temp = "TURN"
                    elif(self.node.level == 1):
                        temp = "RIVER"
                    else:
                        temp = None
                        raise ValueError("Node level out of bounds")

                    new_level = self.node.level + 1
                    child = StepNode(self.node, new_level, self.action, self.node.numPlayers, temp, new_deck, new_history, self.node.irlHand, self.node.roundAverage, self.node.actions, self.node.profile, self.node.risk)
                    child.cardHistory.append(new_card)
                    
                    if(self.node.state == "TURN"):
                        child.actions = ["CALL", "FOLD", "RAISE", "CHECK"]

                    if(child.state == "TURN" or child.state == "RIVER"):
                        child.currentBetAmount = self.node.currentBetAmount * 2
                        child.raiseAmount = self.node.raiseAmount * 2

                        if(self.action == "CALL"):
                            child.pot = self.node.pot + child.currentBetAmount * child.roundAverage * child.numPlayers
                            child.gameBet = self.node.gameBet + child.currentBetAmount * child.roundAverage

                        if(self.action == "RAISE"):
                            child.pot = self.node.pot + (child.currentBetAmount + child.raiseAmount) * child.roundAverage * child.numPlayers
                            child.gameBet = self.node.gameBet + (child.currentBetAmount + child.raiseAmount) * child.roundAverage

                        if(self.action == "FOLD"):
                            child.pot = self.node.pot
                            child.gameBet = self.node.gameBet
                            child.giveUp = True

                        if (self.action == "CHECK"):
                            child.pot = self.node.pot
                            child.gameBet = self.node.gameBet

                    i += 1
                    if lst == None:
                        children.append(child)
                    else:
                        lst.append(child)

                if lst == None:
                    return children
                else:
                    return
        else:
            print("Action node is working in an empty deck")

class StepNode(Node):
    """
    A node holding a state in the tree.
    """
    def __init__(self, parent, level, action, numPlayers, state, deck, cardHistory, irlHand, roundAverage, actions, profile, risk,
                pot = 0, gameBet = 0, currentBetAmount = 0, raiseAmount = 0):
        super(StepNode, self).__init__(parent)
        self.state = state
        self.reward = 0
        self.level = level
        self.creationAction = action
        self.numPlayers = numPlayers
        self.deck = deck
        self.hand = None
        self.cardHistory = cardHistory
        self.irlHand = irlHand
        self.giveUp = False
        self.roundAverage = roundAverage
        self.pot = pot
        self.gameBet = gameBet
        self.currentBetAmount = currentBetAmount
        self.raiseAmount = raiseAmount
        self.actions = actions
        self.profile = profile
        self.risk = risk
    

    def returnRank(self, card):
        return card.getNumericalValue()

    def findBestHand(self, cardList, returnRating = False):
        #print(cardList)
        #cardList = self.flop + self.hand
        possible_hands = itertools.combinations(cardList,5)
        rating = 0
        best = None
        current = 0
        for hand in possible_hands:
            current = self.rateHand(list(hand))
            if current > rating:
                rating = current
                best = hand
        self.hand = best
        if returnRating:
            return rating

    def rateHand(self, hand):
        opt1 = self.checkRanks(hand)
        opt2 = self.checkSequence(hand)
        opt3 = self.checkSuits(hand)
        #if its a high card
        if opt1 == None and opt2 == None and opt3 == None:
            temp = hand
            temp.sort(key=self.returnRank)
            return temp[-1].getNumericalValue() - 1
        #if its a pair/two pairs/three of a kind/four of a kind/full house
        if opt1 != None and opt2 == None and opt3 == None:
            return opt1
        #if its a straight
        if opt1 == None and opt2 != None and opt3 == None:
            return 52 + (opt2.getNumericalValue()-2)
        #if its just a flush 
        if opt1 == None and opt2 == None and opt3 != None:
            return 62 + (opt3.getNumericalValue()-2)
        #if its a flush and repeated cards see which one is higher
        if opt1 != None and opt2 == None and opt3 != None:
            if opt1 > 62 + (opt3.getNumericalValue()-2):
                return opt1
            else:
                return 62 + (opt3.getNumericalValue()-2)
        #if its a flush and a sequence
        if opt1 == None and opt2 != None and opt3 != None:
            #if its a royal flush
            if opt2.getNumericalValue() == 10:
                return 110
            #if its a straight flush
            else:
                return 101 + (opt2.getNumericalValue()-2)
    
    def checkRanks(self, hand):
        repeats = []
        times = []
        for card in hand:
            if card.getNumericalValue() in repeats:
                times[repeats.index(card.getNumericalValue())] += 1
            else:
                repeats.append(card.getNumericalValue())
                times.append(1)
        if len(repeats) == 5:
            return None
        #pair
        if len(repeats) == 4:
            return 14 + (repeats[times.index(2)]-2)
        if len(repeats) == 3:
            #three of a kind
            if 3 in times:
                return 40 + (repeats[times.index(3)]-2)
            #two pair
            else:
                firstRank = repeats[times.index(2)]
                times[times.index(2)] = 0
                secondRank = repeats[times.index(2)]
                if firstRank > secondRank:
                    return 27 + (firstRank -2)
                else:
                    return 27 + (secondRank -2)
        if len(repeats) == 2:
            #four of a kind
            if 4 in times:
                return 88 + (repeats[times.index(4)]-2)
            #full house
            else:
                return 75 + (repeats[times.index(3)]-2)

    def checkSuits(self, hand):
        #clubs diamonds hearts spades
        suits = [0, 0, 0, 0]
        for card in hand:
            if card.getSuit() == "Clubs":
                suits[0] += 1
            elif card.getSuit() == "Diamonds":
                suits[1] += 1
            elif card.getSuit() == "Hearts":
                suits[2] += 1
            elif card.getSuit() == "Spades":
                suits[3] += 1
        if 5 not in suits:
            return None
        else:
            temp = hand
            temp.sort(key=self.returnRank)
            return temp[-1]
    
    def checkSequence(self, hand):
        temp = hand
        temp.sort(key=self.returnRank)
        i = 0
        seq = True
        while i < len(temp) - 1:
            if temp[i].getNumericalValue()+1 != temp[i+1].getNumericalValue():
                seq = False
                break
            else:
                i += 1
        if not seq:
            return None
        else:
            return temp[0]

    def getReward(self):
        if (self.state == "SHOWDOWN" or self.giveUp):
            #print("this is the game bet in get reward: " + str(self.gameBet))
            key = self.findBestHand(self.cardHistory,True)
            #print("yo")
            if (key == self.irlHand): probValue = 1
            else: probValue = ratings.probs[key]
            hrating = math.exp(4*ratings.heuristic[key]/28)
            return self.getHeuristics(probValue, hrating)

    def getHeuristics(self, probability, hrating):
        if self.profile == "Risky":
            return (1/probability) * 0.3 + hrating * 0.4 + self.pot * 0.2 + self.gameBet * 0.2 
        
        elif self.profile == "Safe":
            cenas = probability * 0.6 + hrating * 0.2 + (1/self.pot) * 0.2 + (1/self.gameBet) * 0.6
            return cenas

        elif self.profile == "Balanced":
            return 0.25 * probability + 0.25 * hrating + 0.2 * (self.pot/self.risk) + 0.3 * (1/self.gameBet) + 0.1 * (1/self.numPlayers)

    def find_children(self):
        children = []
        for action in self.untried_actions():
            act = Action(action, self)
            act.sample_state(children)
        return children

    def find_random_child(self):
        action = Action(self.randomChild(),self)
        lst = action.sample_state()
        return random.choice(lst)

    def isTerminal(self):
        if self.level == 3 or self.giveUp:
            return True
        return False 

    def untried_actions(self):
        return self.actions

    def randomChild(self):
        if self.isTerminal():
            return None  # If the game is finished then no moves can be made
        action = random.choice(self.untried_actions())  
        return action 

    def __str__(self):
        return "State: {}".format(self.state)