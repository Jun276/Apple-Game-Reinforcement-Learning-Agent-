import pytest
import numpy as np
from src.board_generator import BoardGenerator

def test_default_shape():
    generator = BoardGenerator()
    board = generator.generate()
    assert board.shape == (10, 17)
    assert np.all(board >= 1) and np.all(board <= 9)

def test_custom_shape():
    generator = BoardGenerator(rows=5, cols=6)
    board = generator.generate()
    assert board.shape == (5, 6)

def test_seed_reproducibility():
    generator = BoardGenerator(rows=10, cols=17)
    board1 = generator.generate(seed=42)
    board2 = generator.generate(seed=42)
    board3 = generator.generate(seed=123)
    
    assert np.array_equal(board1, board2)
    assert not np.array_equal(board1, board3)

def test_custom_probabilities():
    # Only allow 1 and 9 (equal probability)
    probs = [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]
    generator = BoardGenerator(probabilities=probs)
    board = generator.generate(seed=99)
    
    # Check that only 1 and 9 appear on the board
    unique_vals = np.unique(board)
    for val in unique_vals:
        assert val in [1, 9]

def test_invalid_probabilities():
    # Length not equal to 9
    with pytest.raises(AssertionError):
        BoardGenerator(probabilities=[0.5, 0.5])
        
    # Sum not equal to 1.0
    with pytest.raises(AssertionError):
        BoardGenerator(probabilities=[0.1]*9)
