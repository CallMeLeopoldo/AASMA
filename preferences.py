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