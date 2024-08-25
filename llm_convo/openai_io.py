from typing import List, Optional
import os
import openai
os.environ["OPENAI_API_KEY"]="sk-DX1STMau-CZLq9pj-owP5dAHdRxO_M0wFTbxhLoZYDT3BlbkFJgnGIRcZuv0M6OfHdzZbXhhPO1BqPSbV3vprgJj2GYA"

openai.api_key = os.environ["OPENAI_API_KEY"]


class OpenAIChatCompletion:
    def __init__(self, system_prompt: str, model: Optional[str] = None):
        self.system_prompt = system_prompt
        self.model = model

    def get_response(self, transcript: List[str]) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        for i, text in enumerate(reversed(transcript)):
            messages.insert(1, {"role": "user" if i % 2 == 0 else "assistant", "content": text})
        #output = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo" if self.model is None else self.model,
        #    messages=messages,
        #)
       # output = client.chat.completions.create(
       #     model="gpt-3.5-turbo" if self.model is None else self.model,
       #     messages=messages,)
        output = openai.chat.completions.create(
        model="gpt-3.5-turbo" if self.model is None else self.model,
        messages=messages,)

        #return output["choices"][0]["message"]["content"]
        return output.choices[0].message.content
