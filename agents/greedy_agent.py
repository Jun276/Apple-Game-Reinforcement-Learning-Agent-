import numpy as np
from agents.base_agent import BaseAgent

class GreedyAgent(BaseAgent):
    def __init__(self, name="GreedyAgent", seed=None):
        super().__init__(name)
        self.rng = np.random.default_rng(seed)

    def select_action(self, env):
        valid_actions = env.valid_actions
        if not valid_actions:
            raise ValueError("No valid actions available in the environment.")
            
        board = env.board
        action_finder = env.action_finder
        
        max_apples = -1
        best_actions = []
        
        for action in valid_actions:
            y1, x1, y2, x2 = action_finder.action_to_coords(action)
            # Count the number of non-zero apples in this subgrid
            subgrid = board[y1:y2+1, x1:x2+1]
            apple_count = np.count_nonzero(subgrid)
            
            if apple_count > max_apples:
                max_apples = apple_count
                best_actions = [action]
            elif apple_count == max_apples:
                best_actions.append(action)
                
        # Randomly choose one among the tied best actions
        return self.rng.choice(best_actions)
