import numpy as np
import time
import os
from src.apple_env import AppleEnv
from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.ppo_agent import PPOAgent

def evaluate_agent(agent, num_episodes=100):
    """
    Evaluates an agent over a specified number of episodes on deterministic seeds.
    """
    env = AppleEnv(one_hot=True)
    scores = []
    turns = []
    
    start_time = time.time()
    for ep in range(num_episodes):
        # Use seed ep+1 so all agents play on the same boards
        obs, info = env.reset(seed=ep + 1)
        terminated = False
        
        while not terminated:
            action = agent.select_action(env)
            obs, reward, terminated, truncated, info = env.step(action)
            
        scores.append(info["score"])
        turns.append(info["turn_count"])
        
    duration = time.time() - start_time
    
    return {
        "mean_score": np.mean(scores),
        "min_score": np.min(scores),
        "max_score": np.max(scores),
        "mean_turns": np.mean(turns),
        "duration": duration
    }

def main():
    num_episodes = 100
    print(f"Starting evaluation of agents over {num_episodes} episodes...")
    
    random_agent = RandomAgent(seed=42)
    greedy_agent = GreedyAgent(seed=42)
    
    random_results = evaluate_agent(random_agent, num_episodes)
    print(f"Random Agent finished in {random_results['duration']:.2f}s.")
    
    greedy_results = evaluate_agent(greedy_agent, num_episodes)
    print(f"Greedy Agent finished in {greedy_results['duration']:.2f}s.")
    
    # Try evaluating PPO agent if trained model exists
    model_path = "models/ppo_apple_agent.zip"
    ppo_results = None
    if os.path.exists(model_path):
        try:
            ppo_agent = PPOAgent(model_path=model_path)
            ppo_results = evaluate_agent(ppo_agent, num_episodes)
            print(f"PPO Agent finished in {ppo_results['duration']:.2f}s.")
        except Exception as e:
            print(f"Error evaluating PPO Agent: {e}")
    else:
        print("PPO Agent model weights not found. Skipping PPO evaluation.")
    
    # Print Markdown Table
    print("\n### Evaluation Results (100 Episodes)")
    print("| Agent | Mean Score | Min Score | Max Score | Mean Turns | Avg Time/Episode |")
    print("| --- | --- | --- | --- | --- | --- |")
    print(f"| Random | {random_results['mean_score']:.2f} | {random_results['min_score']} | {random_results['max_score']} | {random_results['mean_turns']:.2f} | {random_results['duration']/num_episodes*1000:.1f}ms |")
    print(f"| Greedy | {greedy_results['mean_score']:.2f} | {greedy_results['min_score']} | {greedy_results['max_score']} | {greedy_results['mean_turns']:.2f} | {greedy_results['duration']/num_episodes*1000:.1f}ms |")
    
    if ppo_results is not None:
        print(f"| PPO | {ppo_results['mean_score']:.2f} | {ppo_results['min_score']} | {ppo_results['max_score']} | {ppo_results['mean_turns']:.2f} | {ppo_results['duration']/num_episodes*1000:.1f}ms |")

if __name__ == "__main__":
    main()
