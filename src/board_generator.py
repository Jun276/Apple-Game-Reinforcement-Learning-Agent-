import numpy as np

class BoardGenerator:
    def __init__(self, rows=10, cols=17, probabilities=None):
        """
        board_generator.py - Generates Apple Game boards.
        
        Parameters:
            rows (int): Number of rows (default: 10)
            cols (int): Number of columns (default: 17)
            probabilities (list/array): Probability distribution for digits 1 to 9.
                                        Must be of length 9 and sum to 1.
                                        If None, uniform distribution is used.
        """
        self.rows = rows
        self.cols = cols
        
        # Valid values are integers 1 through 9
        self.values = np.arange(1, 10, dtype=np.int32)
        
        if probabilities is not None:
            probabilities = np.array(probabilities, dtype=np.float32)
            assert len(probabilities) == 9, "Probabilities must have exactly 9 elements."
            assert np.isclose(np.sum(probabilities), 1.0), "Probabilities must sum to 1.0."
            self.probabilities = probabilities
        else:
            self.probabilities = np.ones(9, dtype=np.float32) / 9.0

    def generate(self, seed=None):
        """
        Generates a random board of shape (rows, cols) with specified seed and probabilities.
        """
        if seed is not None:
            rng = np.random.default_rng(seed)
        else:
            rng = np.random.default_rng()
            
        board = rng.choice(
            self.values,
            size=(self.rows, self.cols),
            p=self.probabilities
        )
        return board
