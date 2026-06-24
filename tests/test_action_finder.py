import pytest
import numpy as np
from src.action_finder import ActionFinder, ROWS, COLS

def test_action_space_size():
    finder = ActionFinder(ROWS, COLS)
    # Total pairs of rows: 10 * 11 / 2 = 55
    # Total pairs of cols: 17 * 18 / 2 = 153
    # Total actions = 55 * 153 = 8415
    assert finder.num_actions == 8415

def test_bidirectional_mapping():
    finder = ActionFinder(ROWS, COLS)
    
    # Test first action
    coords_0 = finder.action_to_coords(0)
    assert coords_0 == (0, 0, 0, 0)
    assert finder.coords_to_action(*coords_0) == 0
    
    # Test last action
    last_idx = finder.num_actions - 1
    coords_last = finder.action_to_coords(last_idx)
    assert coords_last == (ROWS - 1, COLS - 1, ROWS - 1, COLS - 1)
    assert finder.coords_to_action(*coords_last) == last_idx
    
    # Test arbitrary action mapping
    for i in [10, 100, 500, 1000, 5000, 8000]:
        coords = finder.action_to_coords(i)
        assert finder.coords_to_action(*coords) == i

def test_prefix_sum_calculation():
    finder = ActionFinder(3, 3)
    board = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    prefix = finder.compute_prefix_sum(board)
    
    # Check shape: (rows + 1, cols + 1)
    assert prefix.shape == (4, 4)
    assert prefix[0, 0] == 0
    assert prefix[1, 1] == 1
    assert prefix[2, 2] == 1 + 2 + 4 + 5
    assert prefix[3, 3] == np.sum(board)
    
    # Check subgrid sum of [5, 6, 8, 9] which is from (1, 1) to (2, 2)
    # Sum should be 5 + 6 + 8 + 9 = 28
    sub_sum = finder.get_subgrid_sum(prefix, 1, 1, 2, 2)
    assert sub_sum == 28

def test_find_valid_actions_empty():
    finder = ActionFinder(ROWS, COLS)
    # Board with all zeros
    board = np.zeros((ROWS, COLS), dtype=np.int32)
    valid_actions = finder.find_valid_actions(board)
    assert len(valid_actions) == 0

def test_find_valid_actions_single():
    finder = ActionFinder(ROWS, COLS)
    board = np.zeros((ROWS, COLS), dtype=np.int32)
    # Place a 3 and a 7 adjacent to each other
    board[2, 3] = 3
    board[2, 4] = 7
    
    valid_actions = finder.find_valid_actions(board)
    
    # The only valid rectangle should be (2, 3) to (2, 4)
    expected_coords = (2, 3, 2, 4)
    expected_action_idx = finder.coords_to_action(*expected_coords)
    
    assert expected_action_idx in valid_actions
    assert len(valid_actions) == 1248  # 24 vertical choices * 52 horizontal choices = 1248

