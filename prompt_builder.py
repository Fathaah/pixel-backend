from utils import load_json_from_file
from pixel_models.prompt_request import PromptRequest
import json
import random

def build_prompt(mini_prompt):
    promptRequest = build_prompt_request_obj(mini_prompt)

    if(promptRequest.filename is None or promptRequest.filename == ""):
        return build_prompt_lora_request_advanced(promptRequest)
    else:
        return build_prompt_lora_ip_request(promptRequest)

def build_prompt_request_obj(mini_prompt):
    print(mini_prompt)
    mini_prompt = json.loads(mini_prompt)
    mini_prompt = PromptRequest(
            prompt=mini_prompt.get("prompt"),
            keywords=mini_prompt.get("keywords"),
            aspect_ratio=mini_prompt.get("aspectRatio"),
            model=mini_prompt.get("model"),
            trigger_word=mini_prompt.get("triggerWord"),
            filename=mini_prompt.get("filename"),
            influence=mini_prompt.get("influence"),
            generation_seed=mini_prompt.get("generationSeed"),
            refine=mini_prompt.get("refine"),
            diffusion_steps=mini_prompt.get("diffusionSteps"),
        )
    return mini_prompt

def build_prompt_lora_request(mini_prompt: PromptRequest):
    prompt = load_json_from_file('workflows/Lora_FreeU.json')
    prompt["6"]["inputs"]["text"] = mini_prompt.prompt + ", " + ", ".join(mini_prompt.keywords) + ", (" + mini_prompt.trigger_word + ":1.3)"
    prompt["11"]["inputs"]["lora_name"] = mini_prompt.model
    w_and_h = get_w_and_h(int(mini_prompt.aspect_ratio.replace(":", "")))
    prompt["5"]["inputs"]["width"] = w_and_h[0]
    prompt["5"]["inputs"]["height"] = w_and_h[1]
    prompt["3"]["inputs"]["seed"] = mini_prompt.generation_seed if (mini_prompt.generation_seed)  else random.randint(0, 0xffffffffffffffff)
    prompt["3"]["inputs"]["steps"] = mini_prompt.diffusion_steps
    if(not mini_prompt.refine):
        prompt["3"]["inputs"]["model"][0] = "11"
    print("Prompt finally is : ", prompt)
    return prompt

def build_prompt_lora_request_advanced(mini_prompt: PromptRequest):
    prompt = load_json_from_file('workflows/lora+freeU+refine+api.json')
    text =  mini_prompt.prompt + ", " + ", ".join(mini_prompt.keywords) + ", (" + mini_prompt.trigger_word + ":1.3)"
    prompt["30"]["inputs"]["text_l"] = text
    prompt["30"]["inputs"]["text_g"] = text
    prompt["40"]["inputs"]["text"] = text
    # HACK
    if 'disney' in mini_prompt.keywords:
        prompt["33"]["inputs"]["text_l"] = 'colorless rendition, extremely poor quality, subpar quality, average quality, awkward cropping, out of focus,realistic photo, bad anatomy, extra hands, extra legs, extra fingers, poorly drawn face, fused face, cloned face, worst feet, extra feet, fused feet, missing fingers, extra fingers, bad fingers, long fingers, short fingers, horn, extra eyes'
        prompt["33"]["inputs"]["text_g"] = 'colorless rendition, extremely poor quality, subpar quality, average quality, awkward cropping, out of focus,realistic photo, bad anatomy, extra hands, extra legs, extra fingers, poorly drawn face, fused face, cloned face, worst feet, extra feet, fused feet, missing fingers, extra fingers, bad fingers, long fingers, short fingers, horn, extra eyes'
        prompt["41"]["inputs"]["text_g"] = 'colorless rendition, extremely poor quality, subpar quality, average quality, awkward cropping, out of focus,realistic photo, bad anatomy, extra hands, extra legs, extra fingers, poorly drawn face, fused face, cloned face, worst feet, extra feet, fused feet, missing fingers, extra fingers, bad fingers, long fingers, short fingers, horn, extra eyes'
    if 'studio' in mini_prompt.keywords:
        prompt["33"]["inputs"]["text_l"] = 'bad fingers, missing fingers, cropped, blurry, low quality, bad hands, missing legs, missing arms, extra fingers, cg, 3d, unreal' 
        prompt["33"]["inputs"]["text_g"] = 'bad fingers, missing fingers, cropped, blurry, low quality, bad hands, missing legs, missing arms, extra fingers, cg, 3d, unreal'
        prompt["41"]["inputs"]["text"] = 'bad fingers, missing fingers, cropped, blurry, low quality, bad hands, missing legs, missing arms, extra fingers, cg, 3d, unreal'
    
    prompt["53"]["inputs"]["lora_name"] = mini_prompt.model
    w_and_h = get_w_and_h(int(mini_prompt.aspect_ratio.replace(":", "")))
    prompt["5"]["inputs"]["width"] = w_and_h[0]
    prompt["5"]["inputs"]["height"] = w_and_h[1]
    prompt["38"]["inputs"]["noise_seed"] = mini_prompt.generation_seed if (mini_prompt.generation_seed)  else random.randint(0, 0xffffffffffffffff)
    prompt["36"]["inputs"]["noise_seed"] = mini_prompt.generation_seed if (mini_prompt.generation_seed)  else random.randint(0, 0xffffffffffffffff)
    # prompt["3"]["inputs"]["steps"] = mini_prompt.diffusion_steps
    # if(not mini_prompt.refine):
    #     prompt["3"]["inputs"]["model"][0] = "11"
    print("Prompt finally is : ", prompt)
    return prompt

def build_prompt_lora_ip_request(mini_prompt):
    prompt = load_json_from_file('workflows/Lora_IPadapter.json')
    prompt["7"]["inputs"]["text"] = mini_prompt.prompt + ", " + ", ".join(mini_prompt.keywords) + ", (" + mini_prompt.trigger_word + ":1.3)"
    prompt["30"]["inputs"]["lora_name"] = mini_prompt.model
    w_and_h = get_w_and_h(int(mini_prompt.aspect_ratio.replace(":", "")))
    prompt["10"]["inputs"]["width"] = w_and_h[0]
    prompt["10"]["inputs"]["height"] = w_and_h[1]
    prompt["9"]["inputs"]["seed"] = mini_prompt.generation_seed if (mini_prompt.generation_seed)  else random.randint(0, 0xffffffffffffffff)
    prompt["9"]["inputs"]["steps"] = mini_prompt.diffusion_steps
    prompt["6"]["inputs"]["image"] = mini_prompt.filename
    prompt["5"]["inputs"]["weight"] = mini_prompt.influence
    if(not mini_prompt.refine):
        prompt["9"]["inputs"]["model"][0] = "5"
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
