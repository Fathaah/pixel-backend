from dataclasses import dataclass, field

@dataclass
class Product:
    id: str
    name: str
    product_type: str
    thumbnail: str
    lora_model_name: str
    trigger_word: str
    user_id: str = "admin"
    