import json
import os

from openai import OpenAI

from . import config
from .tools import TOOL_SCHEMAS

client = OpenAI(
    base_url=config.BASE_URL,
    api_key=config.API_KEY,
)


# System prompt
SYSTEM_PROMPT = f"""
You are a coding agent. Your job is to code.
Use the bash tool to inspect files.
Answer back to user once exploration is done.
"""  # TODO

def call_llm(messages):
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS
    )

    message = response.choices[0].message
    completion_details = response.usage.completion_tokens_details
    prompt_details = response.usage.prompt_tokens_details

    usage = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'reasoning_tokens': getattr(completion_details , 'reasoning_tokens' , None),
        'cached_tokens': getattr(prompt_details , 'cached_tokens' , None)
    }

    return message , usage

if __name__ == "__main__":
    user_input = input('Enter your prompt> ')

    message = call_llm(user_input)

    print('\nAgent: ' , message.content , '\n')