import os
from agents.base_agent import BaseAgent
from sb3_contrib import MaskablePPO
from src.ppo_policy import AppleCNNFeatureExtractor  # Must import so SB3 load finds it

class PPOAgent(BaseAgent):
    def __init__(self, model_path="models/ppo_apple_agent.zip", name="PPOAgent"):
        super().__init__(name)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Trained model not found at {model_path}. Please train PPO first.")
        self.model = MaskablePPO.load(model_path)

    def select_action(self, env):
        # We need the observation
        obs = env._get_obs()
        action_masks = env.action_masks()
        
        # Predict using MaskablePPO
        action, _states = self.model.predict(obs, action_masks=action_masks, deterministic=True)
        return int(action)
