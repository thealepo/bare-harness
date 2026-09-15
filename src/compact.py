from . import config
from .llm import client


SYSTEM_PROMPT = """."""  # TODO

def is_compaction_needed(usage):
    return usage['prompt_token'] > 248_000 * 0.85  # hard-coded numbers. 248k context window, 85% full