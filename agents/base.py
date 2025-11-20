from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, model, role, weight, temperature):
        self.name = name
        self.model = model
        self.role = role
        self.weight = weight
        self.temperature = temperature

    @abstractmethod
    def analyze(self, market_data):
        """
        Analyzes the market data and returns an initial opinion.
        Returns:
            dict: {
                "signal": "BUY" | "SELL" | "HOLD",
                "confidence": float (0.0 - 1.0),
                "reasoning": str
            }
        """
        pass

    @abstractmethod
    def debate(self, context, round_history):
        """
        Participates in the debate loop.
        Args:
            context (str): Summary of the current situation.
            round_history (list): List of previous arguments from other agents.
        Returns:
            dict: {
                "response": str,
                "revised_signal": "BUY" | "SELL" | "HOLD",
                "revised_confidence": float
            }
        """
        pass
