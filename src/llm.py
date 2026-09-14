import json
import os

from openai import OpenAI

from . import config

client = OpenAI(
    bare_url=config.BASE_URL,
    api_key=config.API_KEY,
)


# System prompt
SYSTEM_PROMPT = f"""."""  # TODO

def call_llm(messages , tools=None):
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message
    completion_details = response.usage.completions_tokens_details
    prompt_details = response.usage.prompt_tokens_details

    return message