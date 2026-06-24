import gymnasium as gym
from gymnasium import spaces
import numpy as np
from src.board_generator import BoardGenerator
from src.action_finder import ActionFinder, ROWS, COLS

class AppleEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self, rows=ROWS, cols=COLS, one_hot=True, probabilities=None):
        """
        Apple Game Gymnasium Environment.
        
        Parameters:
            rows (int): Board rows (default: 10)
            cols (int): Board columns (default: 17)
            one_hot (bool): If True, observation space is one-hot encoded (10, rows, cols).
                             If False, observation space is normalized board (1, rows, cols).
            probabilities (list): Probability distribution for digits 1-9.
        """
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.one_hot = one_hot
        
        self.board_generator = BoardGenerator(rows, cols, probabilities)
        self.action_finder = ActionFinder(rows, cols)
        
        # Action space: flat index of all possible subgrids
        self.action_space = spaces.Discrete(self.action_finder.num_actions)
        
        # Observation space
        if self.one_hot:
            # 10 channels representing numbers 0 through 9
            self.observation_space = spaces.Box(
                low=0.0,
                high=1.0,
                shape=(10, self.rows, self.cols),
                dtype=np.float32
            )
        else:
            # Single channel normalized board [0.0, 1.0]
            self.observation_space = spaces.Box(
                low=0.0,
                high=1.0,
                shape=(1, self.rows, self.cols),
                dtype=np.float32
            )
            
        self.board = None
        self.score = 0
        self.turn_count = 0
        self.valid_actions = []

    def reset(self, seed=None, options=None):
        """Resets the environment to an initial state."""
        super().reset(seed=seed)
        
        # Generate board (isolated seeding handled by generator)
        self.board = self.board_generator.generate(seed=seed)
        self.score = 0
        self.turn_count = 0
        
        # Find initial valid actions
        self._update_valid_actions()
        
        return self._get_obs(), self._get_info()

    def step(self, action):
        """Executes one step in the environment."""
        # Convert action (int) to coordinates
        y1, x1, y2, x2 = self.action_finder.action_to_coords(action)
        
        # Check if the action is valid
        if action not in self.valid_actions:
            # Penalty or 0 reward, state remains unchanged
            reward = 0.0
            terminated = (len(self.valid_actions) == 0)
            truncated = False
            return self._get_obs(), reward, terminated, truncated, self._get_info()
            
        # Action is valid:
        # 1. Count non-zero elements in selected rectangle
        subgrid = self.board[y1:y2+1, x1:x2+1]
        removed_apples = np.count_nonzero(subgrid)
        
        # 2. Add to score and reward
        reward = float(removed_apples)
        self.score += removed_apples
        
        # 3. Clear selected cells to 0
        self.board[y1:y2+1, x1:x2+1] = 0
        self.turn_count += 1
        
        # 4. Update valid actions for the next step
        self._update_valid_actions()
        
        # 5. Check termination
        terminated = (len(self.valid_actions) == 0)
        truncated = False
        
        return self._get_obs(), reward, terminated, truncated, self._get_info()

    def action_masks(self):
        """
        Exposes the action mask for MaskablePPO.
        Returns a boolean array of shape (num_actions,) where True indicates a valid action.
        """
        mask = np.zeros(self.action_space.n, dtype=bool)
        mask[self.valid_actions] = True
        return mask

    def _update_valid_actions(self):
        """Computes and updates the list of valid action indices."""
        self.valid_actions = self.action_finder.find_valid_actions(self.board)

    def _get_obs(self):
        """Computes the observation from the current board state."""
        if self.one_hot:
            obs = np.zeros((10, self.rows, self.cols), dtype=np.float32)
            for r in range(self.rows):
                for c in range(self.cols):
                    val = self.board[r, c]
                    obs[val, r, c] = 1.0
            return obs
        else:
            return self.board.reshape(1, self.rows, self.cols).astype(np.float32) / 9.0

    def _get_info(self):
        """Returns diagnostic information."""
        return {
            "score": self.score,
            "remaining_apples": np.count_nonzero(self.board),
            "turn_count": self.turn_count
        }

    def render(self):
        """Renders the environment to a string (ANSI)."""
        output = f"Score: {self.score} | Turns: {self.turn_count} | Apples Left: {np.count_nonzero(self.board)}\n"
        for r in range(self.rows):
            row_str = " ".join(str(val) if val > 0 else "." for val in self.board[r])
            output += row_str + "\n"
        return output
