import os
import gymnasium as gym
from src.apple_env import AppleEnv
from src.ppo_policy import AppleCNNFeatureExtractor
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from stable_baselines3.common.callbacks import CheckpointCallback

def make_env():
    env = AppleEnv(one_hot=True)
    # Wrap environment with ActionMasker for MaskablePPO
    env = ActionMasker(env, lambda e: e.action_masks())
    return env

def main():
    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)
    
    print("Initializing environment...")
    env = make_env()
    
    policy_kwargs = dict(
        features_extractor_class=AppleCNNFeatureExtractor,
        features_extractor_kwargs=dict(features_dim=256),
        net_arch=dict(pi=[128], vf=[128])
    )
    
    print("Setting up MaskablePPO model...")
    model = MaskablePPO(
        MaskableActorCriticPolicy,
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=128,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        verbose=1,
        policy_kwargs=policy_kwargs,
        tensorboard_log=None
    )
    
    total_timesteps = 200000
    print(f"Starting training for {total_timesteps} timesteps on CPU...")
    
    # Callback to save checkpoints
    checkpoint_callback = CheckpointCallback(
        save_freq=50000,
        save_path="./models/checkpoints/",
        name_prefix="ppo_apple_model"
    )
    
    model.learn(
        total_timesteps=total_timesteps,
        callback=checkpoint_callback
    )
    
    # Save final model
    model_path = os.path.join("models", "ppo_apple_agent")
    model.save(model_path)
    print(f"Training completed. Model saved to {model_path}.zip")

if __name__ == "__main__":
    main()
