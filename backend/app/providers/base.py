from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def ask(self, user_message: str, dynamic_system_instruction: str) -> str:
        pass
