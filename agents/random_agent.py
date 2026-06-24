import numpy as np
from agents.base_agent import BaseAgent

class RandomAgent(BaseAgent):
    def __init__(self, name="RandomAgent", seed=None):
        super().__init__(name)
        self.rng = np.random.default_rng(seed)

    def select_action(self, env):
        valid_actions = env.valid_actions
        if not valid_actions:
            raise ValueError("No valid actions available in the environment.")
        return self.rng.choice(valid_actions)
