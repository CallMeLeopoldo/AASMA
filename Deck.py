import random

class Card:

    def __init__(self, value, suit, numVal):
        self.value = value
        self.suit = suit 
        self.name = value + " of " + suit
        self.numVal = numVal
        self.showing = False

    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    def getName(self):
        return self.name

    def getNumericalValue(self):
        return self.numVal
    
    def isShowing(self):
        return self.showing
    
    def turn(self):
        self.showing = True

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
                self.cards.append(Card(value,suit,values[value]))

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
    
    # returns card with card name
    def getCardByName(self, cardName):
        for card in self.cards:
            if cardName == card.getName():
                return card
        return None

    # checks if specific card is in the deck, by the card name
    def containsCard(self, cardName):
        for card in self.cards:
            if cardName == card.getName():
                return True
        return False

    # shuffles the deck
    def shuffle(self):
        random.shuffle(self.cards)
    
    # returns one card from the deck
    def dealCard(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop()
    
