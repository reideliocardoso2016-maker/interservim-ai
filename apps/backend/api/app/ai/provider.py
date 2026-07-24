from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        ...

    @abstractmethod
    async def classify_intent(self, message: str, context: str = "") -> dict:
        ...

    @abstractmethod
    async def generate_marketing_content(self, params: dict) -> dict:
        ...
