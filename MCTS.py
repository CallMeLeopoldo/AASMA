import random
import utils

#################################################
####            MCTS                        #####
#################################################

class MCTS(object):
    def __init__(self, tree_policy, default_policy, backup):
        self.tree_policy = tree_policy
        self.default_policy = default_policy
        self.backup = backup
        self.root = None
    
    def __call__(self,root, n=1500):
        if root.parent is not None:
            raise ValueError("Root's parent must be None.")
        self.root = root
        for _ in range(n):
            node = _get_next_node(self.root, self.tree_policy)
            node.reward = self.default_policy(node)
            self.rollout(node)

        return utils.max(root.children().values) 

    def rollout(self, node):
        path = self._get_next_node(node)
        next_node = path[-1]
        self._simulation(next_node)

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

    def _simulation(self, state_node, action):
        reward = 0
        if state_node.level == 6:
            reward += state_node._calculate_reward()
        else:
            state_node.children[action].sample_state()
            #ideia é criar um novo no random o que quer dizer que temos que criar um modo nos nos se criarem com as caracteristicas
            #IMPORTANTE e preciso ter em atencao o atributo level dos nos que garante se sao ou nao terminais

    def _best_child(self, state_node, tree_policy):
        best_action_node = utils.rand_max(state_node.children.values(),
                                        key=tree_policy)
        return best_action_node.sample_state()


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