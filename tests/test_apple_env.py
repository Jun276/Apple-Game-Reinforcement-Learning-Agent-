import pytest
import numpy as np
import gymnasium as gym
from src.apple_env import AppleEnv

def test_env_initialization():
    # Test one_hot = True
    env_oh = AppleEnv(one_hot=True)
    assert env_oh.action_space.n == 8415
    assert env_oh.observation_space.shape == (10, 10, 17)
    
    # Test one_hot = False
    env_raw = AppleEnv(one_hot=False)
    assert env_raw.observation_space.shape == (1, 10, 17)

def test_env_reset():
    env = AppleEnv(one_hot=True)
    obs, info = env.reset(seed=42)
    
    assert obs.shape == (10, 10, 17)
    assert info["score"] == 0
    assert info["turn_count"] == 0
    assert info["remaining_apples"] == 10 * 17  # Initially all non-zero
    assert env.board is not None

def test_action_mask():
    env = AppleEnv(one_hot=True)
    env.reset(seed=42)
    
    mask = env.action_masks()
    assert mask.shape == (8415,)
    assert mask.dtype == bool
    
    # The number of True values in mask must equal len(env.valid_actions)
    assert np.sum(mask) == len(env.valid_actions)

def test_invalid_step():
    env = AppleEnv(one_hot=True)
    env.reset(seed=42)
    
    initial_board = env.board.copy()
    
    # Find an action that is NOT valid
    mask = env.action_masks()
    invalid_actions = np.where(~mask)[0]
    
    if len(invalid_actions) > 0:
        invalid_action = invalid_actions[0]
        obs, reward, terminated, truncated, info = env.step(invalid_action)
        
        assert reward == 0.0
        assert np.array_equal(env.board, initial_board)
        assert info["score"] == 0
        assert info["turn_count"] == 0

def test_valid_step():
    env = AppleEnv(one_hot=True)
    env.reset(seed=42)
    
    # Find a valid action
    mask = env.action_masks()
    valid_actions = np.where(mask)[0]
    
    assert len(valid_actions) > 0
    valid_action = valid_actions[0]
    
    # Get expected coordinates
    y1, x1, y2, x2 = env.action_finder.action_to_coords(valid_action)
    
    # Count expected removed apples
    subgrid = env.board[y1:y2+1, x1:x2+1]
    expected_removed = np.count_nonzero(subgrid)
    
    obs, reward, terminated, truncated, info = env.step(valid_action)
    
    assert reward == float(expected_removed)
    assert info["score"] == expected_removed
    assert info["turn_count"] == 1
    # Check that cells are indeed cleared to 0
    assert np.all(env.board[y1:y2+1, x1:x2+1] == 0)

def test_rendering():
    env = AppleEnv(one_hot=True)
    env.reset(seed=42)
    render_str = env.render()
    
    assert "Score: 0" in render_str
    assert "Turns: 0" in render_str
    assert len(render_str.split("\n")) == 12  # Header + 10 rows + trailing empty line
