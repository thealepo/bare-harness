import json

from .llm import SYSTEM_PROMPT , call_llm
from .tools import TOOLS
from .ui import ui

ui.banner()
user_input = ui.ask()
if user_input:
    ui.user(user_input)

messages = [
    {'role': 'system' , 'content': SYSTEM_PROMPT},
    {'role': 'user' , 'content': user_input}
]

while True:
    with ui.working():
        message, usage = call_llm(messages)
    messages.append(message.model_dump(exclude_none=True))

    if message.content:
        ui.agent(message.content)

    # stop loop if no tools
    if not message.tool_calls:
        break

    # invoke tool calls
    for tool_call in message.tool_calls or []:
        args = json.loads(tool_call.function.arguments)
        result = TOOLS[tool_call.function.name](**args)
        
        ui.tool(tool_call.function.name, args, result)

        messages.append({
            'role': 'tool',
            'tool_call_id': tool_call.id,
            'content': result
        })

    ui.usage(usage)
