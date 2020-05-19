import random
import utils
import math
import Agent
from Deck import Deck
from Deck import Card
from collections import defaultdict
#################################################
####            MCTS                        #####
#################################################

class MCTS(object):
    def __init__(self):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = 0.5       
        self.root = None
        self.deck = None
        self.hand = None

    def rollout(self, node):
        path = self.select(node)
        print(path)
        leaf = path[-1]
        self.expand(leaf)
        reward = self.simulate(leaf)
        print(path)
        print("this is reward")
        print(reward)
        self.backPropagate(path, reward)
        print(len(self.children[node][0]))

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.isTerminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            print("this is unexplored")
            print(unexplored)
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    #def simulation(self, state_node):
    #    test_node = state_node
    #    while !(test_node.level == 6 or (test_node.isInstance(ActionNode) and test_node.action = "FOLD")):
    #        test_node.sample_state()
    #        new_child = state_node._randomChild()
    #        test_node = new_child
    #    return test_node

    def expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()
        print(len(self.children[node]))

    def simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        i = 0
        print("simulation started")
        while True:
            if node.isTerminal():
                print(":3c")
                reward = node.getReward()
                return reward
            node = node.find_random_child()
            i += 1

    def backPropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)



        #ACTIONNODE -> ACTIONNODE

        #STATENODE -> ACTIONNODE -> STATENODE