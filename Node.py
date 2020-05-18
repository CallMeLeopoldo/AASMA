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
                self.node.cardHistory.append(new_card)
                #POSSIBLE TODO: Make sure the probability of hand to show impacts the heuristic
                #self.node.findBestHand(self.node.cardHistory)
                if(self.level == 1):
                    child = StepNode(node,"TURN", new_deck, self.node.cardHistory)
                elif(self.level == 3):
                    child = StepNode(node,"RIVER", new_deck, self.node.cardHistory)
                elif(self.level == 5):
                    child = StepNode(node,"SHOWDOWN", new_deck, self.node.cardHistory)
                child.level = self.level + 1
                return child
        else:
            print("Action node is working in an empty deck")

class StepNode(Node):
    """
    A node holding a state in the tree.
    """
    def __init__(self, parent, deck, cardHistory, state):
        super(StepNode, self).__init__(parent)
        self.state = state
        self.reward = 0
        self.level = 0
        self.deck = deck
        self.hand = None
        self.cardHistory = cardHistory
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
        possible_hands = itertools.combinations(cardList,5)
        rating = 0
        best = None
        current = 0
        for hand in possible_hands:
            curent = rateHand(hand)
            if current > rating:
                rating = current
                best = hand
        self.hand = best

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
            if card.getValue() in repeats:
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
                times.pop(firstRank)
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
        while i < len(temp):
            if temp[i].getNumericalValue() != (temp[i+1].getNumericalValue() + 1):
                seq = False
                break
            else:
                i += 1
        if not seq:
            return None
        else:
            return temp[0]

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