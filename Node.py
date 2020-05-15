import Agent from Agent
import Deck from Deck
import Card from Deck
import random
import itertools

class Node(object):
    def __init__(self, parent, deck, hand):
        self.parent = parent
        self.children = []
        self.q = 0
        self.n = 0
        self.level = 0
        self.deck = deck
        self.hand = hand
        #self.visited = false

    def _isTerminal(self):
        if self.level == 6:
            return True
        return False

    def untried_actions(self):
        return [a for a in self.children if self.children[a].n == 0]
    
    def _randomChild(self):
        return random.choice(self.untried_actions())
        

class Action():
    """
    A node holding an action in the tree.
    """
    def __init__(self, action, ammount, utility, giveUp):
        self.action = action
        self.currentAmmount = ammount
        self.utility = utility or 0 #may be useful
        self.giveUp = giveUp

    def sample_state(self, real_world=False):
        if  not self.deck.isEmpty():
            i = 0
            while i < len(self.deck().getCards()): 
                new_card = self.deck().getCards()[i]
                new_deck = self.deck
                new_deck.removeCard(new_card.getName())
                new_hand = self.findHand(self.hand.append(new_card))
                if(self.level == 1):
                    child = StepNode(self, new_deck, new_hand, "TURN")
                elif(self.level == 3):
                    child = StepNode(self, new_deck, new_hand, "RIVER")
                elif(self.level == 5):
                    child = StepNode(self, new_deck, new_hand, "SHOWDOWN")
                child.level = self.level + 1
                return child
        else:
            print("Action node is working in an empty deck")

class StepNode(Node):
    """
    A node holding a state in the tree.
    """
    def __init__(self, parent, deck, hand, state,):
        super(StepNode, self).__init__(parent)
        self.state = state
        self.reward = 0
    
    def find_children(self,):
        for action in state.actions:
            act = Action(self, action)
            newState = act.sample_state()
            self.children[action] = newState

    def findHand(self, cardList):
        possible_hands = itertools(cardList, 5)
        rating = 0
        best = None
        current = 0
        for hand in possible_hands:
            curent = rateHand(hand)
            if current > rating:
                rating = current
                best = hand
        return best

    def rateHand(self, hand):
        #rules for the hands. use a liner rating here
        pass

    def untried_actions(self, value):
        raise ValueError("Untried actions can not be set.")

    def __str__(self):
        return "State: {}".format(self.state)