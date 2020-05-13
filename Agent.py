from enum import Enum
from queue import Queue
from Chips import Chips
import utils
import random

class Desire(Enum):
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    FOLD = "fold"

class Action(Enum):
    NONE = "none"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    FOLD = "fold"
    SHOWHAND = "show hand"
    PAYBLIND = "pay blind"



class Agent:
    desire = Desire.CALL
    action = Action.NONE
    plan = Queue.queue 

    def __init__(self, identifier):
        self.id = identifier
        self.money = Chips(5000)
    
#################################################
####            DECISION-MAKING             #####
#################################################


#################################################
####         REACTIVE BEHAVIOUR             #####
#################################################

    def agentReactiveDecision(self):
        pass

#################################################
####            COMMUNICATION               #####
#################################################

    def updateBeliefs(self):
        pass

    def sendMessage(self):
        table.sendMessage()

        #sendMessage(Chips, "Fold")
        #sendMessage(Card)
        #sendMessage(2 Cards)

        #receiveMessage(Chips, "Fold")
        #receiveMessage(Card)
        #receiveMessage(2 Cards)

#################################################
####            AUXILIARY               #########
#################################################

    def buildPathPlan():
        pass

#################################################
####            SENSORS                     #####
#################################################

    def checkMyCards(self):
        return self.cards

    def checkTableCards():
        return table.cards
    
    def checkTurn():
        return table.turn
    
    def checkMyChips(self):
        return self.money.getCurrent()
    
    def checkTheirChips(self):
        chips = []
        for agent in table.agents:
            chips.add(agent.cards)
        return chips
    
    def checkPot():
        return table.pot

    def checkBlind():
        return table.blind

    def checkPlayRecords():
        pass

    def checkProfiles():
        pass

    def checkEnvironment():
        pass


#################################################
####            MCTS                        #####
#################################################

class MCTS(object):
    def __init__(self, tree_policy, default_policy, backup):
        self.tree_policy = tree_policy
        self.default_policy = default_policy
        self.backup = backup
    
    def __call__(self,root, n=1500):
        if root.parent is not None:
            raise ValueError("Root's parent must be None.")
        for _ in range(n):
            node = _get_next_node(root, self.tree_policy)
            node.reward = self.default_policy(node)
            self.backup(node)

        return utils.max(root.children().values) 
  
def _expand(state_node):
    action = random.choice(state_node.untried_actions)
    #action = state_node.priority()
    #TODO: Instead of expanding a node randomly, come up with a 
    #priority list where he will first check the actions in a optimist or pessimist way:
    # Optimist way -> Raise, Call, Check, Fold
    # Pessimist way -> Fold, Check, Call, Raise
    # Random way -> Pick randomly
    # Heuristic -> Define a well though out way for choosing depending on the probability of a certain hand and money in possesion 
    return state_node.children[action].sample_state()


def _best_child(state_node, tree_policy):
    best_action_node = utils.rand_max(state_node.children.values(),
                                      key=tree_policy)
    return best_action_node.sample_state()


def _get_next_node(state_node, tree_policy):
    while not state_node.state.is_terminal():
        if state_node.untried_actions:
            return _expand(state_node)
        else:
            state_node = _best_child(state_node, tree_policy)
    return state_node