from utils import load_json_from_file
from pixel_models.prompt_request import PromptRequest
import json
import random

def build_prompt(mini_prompt):
    print(mini_prompt)
    mini_prompt = json.loads(mini_prompt)
    mini_prompt = PromptRequest(
            prompt=mini_prompt.get("prompt"),
            keywords=mini_prompt.get("keywords"),
            aspect_ratio=mini_prompt.get("aspectRatio"),
            model=mini_prompt.get("model"),
            trigger_word=mini_prompt.get("triggerWord")
        )
    prompt = load_json_from_file('workflows/Lora_FreeU.json')
    prompt["6"]["inputs"]["text"] = mini_prompt.prompt + ", " + ", ".join(mini_prompt.keywords) + ", (" + mini_prompt.trigger_word + ":1.3)"
    prompt["11"]["inputs"]["lora_name"] = mini_prompt.model
    w_and_h = get_w_and_h(int(mini_prompt.aspect_ratio.replace(":", "")))
    prompt["5"]["inputs"]["width"] = w_and_h[0]
    prompt["5"]["inputs"]["height"] = w_and_h[1]
    prompt["3"]["inputs"]["seed"] = random.randint(0, 0xffffffffffffffff)
    print("Prompt finally is : ", prompt)
    return prompt

def get_w_and_h(ar):
    if ar == 11:
        return (1024, 1024)
    elif ar == 43:
        return (1182, 886)
    elif ar == 169:
        return (1365, 768)    
    else:
        return (728, 728)  # Default return value for unknown aspect ratios
