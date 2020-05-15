import Agent from Agent
import Deck from Deck
import Card from Deck

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
    
    def _randomChild(self)
        return random.choice(node.untried_actions)
        

class ActionNode(Node):
    """
    A node holding an action in the tree.
    """
    def __init__(self, parent, action):
        super(ActionNode, self).__init__(parent)
        self.action = action
        self.n = 0

    def findHand(cardList):
        possible_hands = itertools(cardList, 5)
        rating = 0
        best = None
        for hand in possible_hands:
            curent = rateHand(hand)
            if current > rating:
                rating = current
                best = hand
        return best
    
    def rateHand(hand):
        #rules for the hands. use a liner rating here
        pass

    def sample_state(self, real_world=False):
        if !deck.isEmpty():
            i = 0
            while i < len(self.deck().getCards()) 
                new_card = self.deck().getCards()[i]
                new_deck = self.deck
                new_deck.removeCard(new_card.getName())
                new_hand = self.findHand(self.hand.append(new_card))
                if(self.level == 1):
                    child = StepNode(self,"TURN", new_deck, new_hand)
                elif(self.level == 3):
                    child = StepNode(self,"RIVER", new_deck, new_hand)
                elif(self.level == 5):
                    child = StepNode(self,"SHOWDOWN", new_deck, new_hand)
                child.level = self.level + 1
        else:
            print("Action node is working in an empty deck")


class StepNode(Node):
    """
    A node holding a state in the tree.
    """
    def __init__(self, parent, state, deck, hand):
        super(StepNode, self).__init__(parent)
        self.state = state
        self.reward = 0
        for action in state.actions:
            self.children[action] = ActionNode(self, action)

    def untried_actions(self, value):
        raise ValueError("Untried actions can not be set.")

    def __str__(self):
        return "State: {}".format(self.state)