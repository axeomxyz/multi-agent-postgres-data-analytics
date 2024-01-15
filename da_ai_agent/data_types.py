import time
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Chat:
    from_name: str
    to_name: str
    message: str
    created: int = field(default_factory=time.time)


@dataclass
class ConversationResult:
    success: bool
    messages: List[Chat]
    cost: float
    tokens: int
    last_message_str: str
    error_message: str


@dataclass
class TurboTool:
    name: str
    config: dict
    function: Callable
