import random
import utils
import Node from Node
import Agent from Agent
import Deck from Deck
import Card from Deck

#################################################
####            MCTS                        #####
#################################################

class MCTS(object):
    def __init__(self, tree_policy, default_policy, backup):
        self.tree_policy = tree_policy
        self.default_policy = default_policy
        self.backup = backup
        self.root = None
        self.deck = None
        self.hand = None
    
    def __call__(self, n=1500, root, deck, hand):
        if root.parent is not None:
            raise ValueError("Root's parent must be None.")
        self.root = root
        self.deck = deck
        self.hand = hand
        for _ in range(n):
            self.rollout(node)
        #    node = _get_next_node(self.root, self.tree_policy)
        #    node.reward = self.default_policy(node)

        #return utils.max(root.children().values)
        # this is to return the best child. adjust accordingly 

    def rollout(self, node):
        path = self._get_next_node(node)
        next_node = path[-1]
        leaf = self._simulation(next_node)
        reward = leaf.calculate_reward()
        self._backPropagate(leaf, reward)

    def select(self, node, tree_policy):
        #order is raise call check fold
        _preference = []
        # Heuristic -> Define a well though out way for choosing depending on the probability of a certain hand and money in possesion 
        if tree_policy == 3:
            pass
        # Random way -> Pick randomly
        elif tree_policy == 2: 
            return random.choice(node.untried_actions)
        else:
            for child in node.untried_actions:
                if child.state == "RAISE" and len(_raise) == 1:
                    _preference.insert(0,child)
                elif child.state == "CALL" and len(_call) == 1:
                    _preference.insert(1,child)
                elif child.state == "CHECK" and len(_check) == 1:
                    _preference.insert(2,child)
                elif child.state == "FOLD" and len(_fold) == 1:
                    _preference.insert(3,child)
            # Optimist way -> Raise, Call, Check, Fold
            if tree_policy == 0:
                return _preference[0]
            # Pessimist way -> Fold, Check, Call, Raise
            else:
                return _preference[-1]

    def _expand(self, state_node, action):
        #return state_node.children[action].sample_state()
        state_node.children[action].n += 1
        #LIL' DOUBT

    def _simulation(self, state_node):
        test_node = state_node
        while !(test_node.level == 6 or (test_node.isInstance(ActionNode) and test_node.action = "FOLD")):
            test_node.sample_state()
            new_child = state_node._randomChild()
            test_node = new_child
        return test_node

    def _best_child(self, state_node, tree_policy):
        best_action_node = utils.rand_max(state_node.children.values(),
                                        key=tree_policy)
        return best_action_node.sample_state()

    def _backPropagate(self, leaf_node, reward_value):
        if leaf_node.parent == None:
            leaf_node.parent.update(leaf_node,reward_value)
            return
        leaf_node.parent.update(leaf_node,reward_value)
        self._backPropagate(leaf_node.parent, reward_value)

    def _get_next_node(self, state_node, tree_policy):
        path = []
        while not state_node.state.is_terminal():
            if state_node.untried_actions:
                if len(state_node.untried_actions) == 1:
                    path.append(state_node.untried_actions[0])
                else:
                    action = self._selection(state_node, tree_policy)
                    self._expand(state_node, action)
                    path.append()
                return path
            else:
                state_node = self._best_child(state_node, tree_policy)
        return state_node



        #ACTIONNODE -> ACTIONNODE

        #STATENODE -> ACTIONNODE -> STATENODE