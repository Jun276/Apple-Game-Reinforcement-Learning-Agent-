from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name="BaseAgent"):
        self.name = name

    @abstractmethod
    def select_action(self, env):
        """
        Selects an action index given the environment state.
        
        Parameters:
            env (AppleEnv): The current game environment.
                            We pass the env object so agents can access both observation,
                            raw board, action masks, etc. as needed.
        Returns:
            action (int): Flat index of the chosen action.
        """
        pass
