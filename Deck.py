import random

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit 
        self.name = value + " of " + suit

    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    def getName(self):
        return self.name
    
    # checks whether other card is the same as this card
    def isEqual(self, other):
        if other.value == self.value and other.suit == self.suit:
            return True
        return False

class Deck:

    def __init__(self):
        self.cards = []
        suits = ["Clubs", "Spades", "Hearts", "Diamonds"] #FIXME ? currently doesnt have a joker
        values = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jack":11,"Queen":12,"King":13,"Ace":14}

        for suit in suits:
            for value in values:
                self.cards.append(Card(value,suit))

    # returns the deck
    def getCards(self):
        return self.cards
    
    # returns the current number of cards in the deck
    def numberCards(self):
        return len(self.cards)

    # checks whether the deck is empty or not
    def isEmpty(self):
        if len(self.cards) > 0:
            return False
        else:
            return True

    # shuffles the deck
    def shuffle(self):
        random.shuffle(self.cards)
    
    # returns one card from the deck
    def dealCard(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop()
