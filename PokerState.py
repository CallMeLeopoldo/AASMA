
from __future__ import division
from __future__ import print_function

import numpy as np
from scipy.stats import rv_discrete, entropy
from copy import deepcopy


class PokerAction(object):
    def __init__(self, action):
        self.action = action
        #self.bet = bet

    def __hash__(self):
        return int(self._hash)

    def __eq__(self, other):
        return (self.action == other.action).all()

    def __str__(self):
        return str(self.action)

    def __repr__(self):
        return str(self.action)


class TableWorld(object):
    def __init__(self, size, information_gain, goal, manual):
        self.size = np.asarray(size)
        self.information_gain = information_gain
        self.goal = np.asarray(goal)
        self.manual = manual


class TableWorldState(object):
    def __init__(self, pos, world, gameState, belief=None):
        self.world = world
        self.deck = deck
        self.actions = ["CALL", "RAISE", "FOLD", "CHECK"]
        self.gameState = gameState
        if belief:
            self.belief = belief
        else:
            self.belief = dict((a, str(0)) for a in self.actions)

    def perform(self, action):
        # get distribution about outcomes
        belief = deepcopy(self.belief)
        belief[action] += 1

        #calculate probabiities according to card shown in the table

        # build next state
        deck.dealCard()
        return TableWorldState(self.world, belief, deck)

    def is_terminal(self):
        return False

    def __eq__(self, other):
        return (self.gameState == other.gameState).all()

    def __hash__(self):
        pass

    def __str__(self):
        return str(self.gameState + " POT: " + "TABLE CARDS: ")

    def __repr__(self):
        return str(self.pos)

    def reward(self, parent, action):
        if (self.gameState == "SHOWDOWN").all():
            print("g", end="")
            return 100
        else:
            reward = -1
            if self.world.information_gain:
                for a in self.actions:
                    reward += entropy(parent.belief[a], self.belief[a])
            return reward