import json
import os

from openai import OpenAI

from . import config

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

def call_llm(messages , tools=None):
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        tools=tools
    )

    return response.choices[0].message

if __name__ == "__main__":
    user_input = input('Enter your prompt> ')

    message = call_llm(user_input)

    print('\nAgent: ' , message.content , '\n')