import os
from openai import OpenAI

class PromptEnhancer:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)

    def enhance_prompt(self, prompt, item):

        prompt = f"Enhance the prompt for a text to image diffusion model for an advertisment for {item} under 40 words: {prompt}"
        
        response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ]
        )
        enhanced_prompt = response.choices[0].message.content.strip()
        return enhanced_prompt