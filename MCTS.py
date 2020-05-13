import random

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

    def rollout(self, note):
        path = self._get_next_node(node)
        next_node = path[-1]
        self._expand(next_node)
        self._simulation(next_node)

    def select(self, node, tree_policy):
        #order is raise call check fold
        _preference = []
        # Heuristic -> Define a well though out way for choosing depending on the probability of a certain hand and money in possesion 
        if tree_policy == 3:
            pass
        # Random way -> Pick randomly
        elif tree_policy == 2:
            n = len(node.untried_actions)
            i = random.randint(0, n-1)
            return node.untried_actions[i]
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

    def _expand(self, state_node):
        self.children[node] = node.children

    def _simulation(self, node):
        reward = 0
        if node.level == 3:
            reward += node._calculate_reward()
        else:
            pass
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
                if len(untried_actions) == 1:
                    path.append(untried_actions[0])
                else:
                    path.append(self._selection(state_node, tree_policy))
                return path
            else:
                state_node = self._best_child(state_node, tree_policy)
        return state_node