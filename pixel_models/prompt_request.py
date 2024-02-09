from dataclasses import dataclass, field
from typing import List

@dataclass
class PromptRequest:
    prompt: str
    trigger_word: str
    keywords: List[str] = field(default_factory=list)
    aspect_ratio: str = "1:1"
    model: str = "lv-000009.safetensors"
    type: str = "lora"
    