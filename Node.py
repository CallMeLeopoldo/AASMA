from Deck import Deck
from Deck import Card
import random
import itertools

class Node(object):
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.q = 0
        self.n = 0
        #self.visited = false

    def isTerminal(self):
        "Returns True if the node has no children"
        return True  

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    def find_children(self):
        "All possible successors of this board state"
        return set()    

    def untried_actions(self):
        return None
    
    def randomChild(self):
        return None
        

class Action():
    """
    A node holding an action in the tree.
    """
    def __init__(self, action, node):
        self.action = action
        self.node = node

    def sample_state(self):
        if  not self.node.deck.isEmpty():
            i = 0
            while i < len(self.node.deck.getCards()): 
                new_card = self.node.deck.getCards()[i]
                new_deck = self.node.deck
                new_deck.removeCard(new_card.getName())
                print(new_card)
                self.node.hand.append(new_card)
                new_hand = self.node.findBestHand(self.node.hand)
                if(self.level == 1):
                    child = StepNode(node,"TURN", new_deck, new_hand)
                elif(self.level == 3):
                    child = StepNode(node,"RIVER", new_deck, new_hand)
                elif(self.level == 5):
                    child = StepNode(node,"SHOWDOWN", new_deck, new_hand)
                child.level = self.level + 1
                return child
        else:
            print("Action node is working in an empty deck")

class StepNode(Node):
    """
    A node holding a state in the tree.
    """
    def __init__(self, parent, deck, hand, state):
        super(StepNode, self).__init__(parent)
        self.state = state
        self.reward = 0
        self.level = 0
        self.deck = deck
        self.hand = hand
        #self.flop = flop
        self.giveUp = False
    
    def find_children(self):
        children = []
        for action in self.untried_actions():
            act = Action(action, self)
            newState = act.sample_state()
            children.append(newState)
        return children

    def find_random_child(self):
        action = self.randomChild()
        return action.sample_state(self)

    def findBestHand(self, cardList):
        print(cardList)
        #cardList = self.flop + self.hand
        #PERGUNTAR À EVANS SE ESTE POSSIBLE HANDS É AS COMBINAÇÕES POSSIVEIS COM AS CARTAS QUE TENHO OU NÃO
        possible_hands = itertools.product(cardList)
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
        #rules for the hands. use a linear rating here
        pass

    def getReward(self):
        if (self.state == "SHOWDOWN"):
            return 100
        else:
            reward = -1
            if True:
                pass
            return reward

    def isTerminal(self):
        if self.level == 6 or self.giveUp:
            return True
        return False  

    def untried_actions(self):
        return ["CALL", "RAISE", "FOLD", "CHECK"]

    def randomChild(self):
        if self.isTerminal():
            return None  # If the game is finished then no moves can be made        
        return random.choice(self.untried_actions())    

    def __str__(self):
        return "State: {}".format(self.state)