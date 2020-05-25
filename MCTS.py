##########################################################################
# MCTS implements the Monte Carlo Tree Search Algorithm.
# The number of rollouts is controlled in class Agent. MCTS does not
# receive anything of its state to agents.
##########################################################################

import random
import utils
import math
import Agent
import copy
from Deck import Deck
from Deck import Card
from collections import defaultdict


class MCTS(object):
    def __init__(self):
        self.Q = defaultdict(int)  # total reward
        self.N = defaultdict(int)  # total visit count
        self.children = dict()  # children
        self.exploration_weight = 0.5       
        self.root = None
        self.deck = None
        self.hand = None
        self.nodesSelected = 0
        self.nodesExpanded = 0

    def rollout(self, node):
        path = self.select(node)
        leaf = path[-1]
        self.expand(leaf)
        reward = self.simulate(leaf)
        self.backPropagate(path, reward)

    def choose(self, node, canCheck, canRaise):
        if node.isTerminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            #avoid unseen moves
            if self.N[n] == 0:
                return float("-inf")  
            return self.Q[n] / self.N[n]

        return max(self.children[node], key=score)

    def select(self, node):
        path = []
        while True:
            path.append(node)
            # node is either unexplored or terminal
            if node not in self.children or not self.children[node]:
                self.nodesSelected += 1
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                self.nodesSelected += 1
                return path
            self.nodesSelected += 1
            #go down to the following layer
            node = self._uct_select(node)  


    def expand(self, node):
        # already expanded
        if node in self.children:
            return 
        if node.isTerminal():
            self.children[node] = []
        else: 
            self.children[node] = node.find_children()


    def simulate(self, node):
        i = 0
        while True:
            if node.isTerminal():
                reward = node.getReward()
                return reward
            node = node.find_random_child()
            i += 1


    def backPropagate(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward


    def _uct_select(self, node):
        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            #Upper Confidence Bound
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)