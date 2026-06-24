import numpy as np

# Default board size
ROWS = 10
COLS = 17

def generate_action_list(rows=ROWS, cols=COLS):
    """
    Generates a deterministic list of all possible rectangular selections (actions)
    on a grid of size (rows, cols).
    Returns a list of tuples: (y1, x1, y2, x2)
    where (y1, x1) is the top-left corner and (y2, x2) is the bottom-right corner.
    """
    actions = []
    for y1 in range(rows):
        for x1 in range(cols):
            for y2 in range(y1, rows):
                for x2 in range(x1, cols):
                    actions.append((y1, x1, y2, x2))
    return actions

# Precompute for default 10x17 board to enable O(1) mappings
DEFAULT_ACTIONS = generate_action_list(ROWS, COLS)
DEFAULT_ACTION_TO_INDEX = {coords: idx for idx, coords in enumerate(DEFAULT_ACTIONS)}

class ActionFinder:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        
        if rows == ROWS and cols == COLS:
            self.actions = DEFAULT_ACTIONS
            self.action_to_index_map = DEFAULT_ACTION_TO_INDEX
        else:
            self.actions = generate_action_list(rows, cols)
            self.action_to_index_map = {coords: idx for idx, coords in enumerate(self.actions)}
            
        self.num_actions = len(self.actions)

    def action_to_coords(self, action_idx):
        """Maps a flat action index to (y1, x1, y2, x2) coordinates."""
        return self.actions[action_idx]

    def coords_to_action(self, y1, x1, y2, x2):
        """Maps coordinates (y1, x1, y2, x2) to a flat action index."""
        return self.action_to_index_map[(y1, x1, y2, x2)]

    def compute_prefix_sum(self, board):
        """
        Computes the 2D prefix sum array of the board.
        board: 2D numpy array of shape (rows, cols)
        Returns:
            prefix_sum: 2D numpy array of shape (rows + 1, cols + 1)
        """
        prefix_sum = np.zeros((self.rows + 1, self.cols + 1), dtype=np.int32)
        # We can compute this using dynamic programming
        for r in range(self.rows):
            for c in range(self.cols):
                prefix_sum[r + 1][c + 1] = (
                    board[r][c]
                    + prefix_sum[r][c + 1]
                    + prefix_sum[r + 1][c]
                    - prefix_sum[r][c]
                )
        return prefix_sum

    def get_subgrid_sum(self, prefix_sum, y1, x1, y2, x2):
        """
        Computes the sum of elements in the rectangle (y1, x1) to (y2, x2) inclusive
        using the precomputed prefix sum array in O(1) time.
        """
        return (
            prefix_sum[y2 + 1][x2 + 1]
            - prefix_sum[y1][x2 + 1]
            - prefix_sum[y2 + 1][x1]
            + prefix_sum[y1][x1]
        )

    def find_valid_actions(self, board):
        """
        Finds all action indices that sum to exactly 10 on the given board.
        board: 2D numpy array of shape (rows, cols)
        Returns:
            valid_action_indices: list of ints (indices in self.actions)
        """
        prefix_sum = self.compute_prefix_sum(board)
        valid_indices = []
        
        for idx, (y1, x1, y2, x2) in enumerate(self.actions):
            # Check sum of the rectangle
            grid_sum = self.get_subgrid_sum(prefix_sum, y1, x1, y2, x2)
            if grid_sum == 10:
                # Extra check: to make sure it is not just a rectangle of all zeros
                # (although a sum of 0 is not 10, so this is naturally covered).
                # But wait, are there any other constraints?
                # The rule states: "제거된 사과는 영구 삭제... 제거된 칸은 0으로 처리... 합 계산 시 0 포함".
                # If the sum is 10, it must contain at least one non-zero apple.
                # A sum of exactly 10 guarantees there is at least one non-zero element since apples are >= 1.
                valid_indices.append(idx)
                
        return valid_indices
