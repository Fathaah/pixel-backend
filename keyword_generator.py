import os
from openai import OpenAI

class KeywordGenerator:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)

    def generate_keywords(self, item):

        prompt = f"Write keywords for generating an advertisement image for a(n) {item} with a text to image stable diffusion model the keywords should be mostly around the setting in which the item should be present for a appealing advertisement. Only return the keywords separated by commas as simple text."
        response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ]
        )
        keywords = response.choices[0].message.content.strip().split(',')
        for i in range(len(keywords)):
            keywords[i] = keywords[i].strip()
        return keywords