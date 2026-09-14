import json
import subprocess


def bash(command):
    result = subprocess.run(command , shell=True , capture_output=True , text=True)
    return result.stdout + result.stderr

def read_file(path):
    with open(path) as f:
        return f.read()

def write_file(path , content):
    with open(path) as f:
        f.write(content)
    return f'Wrote {path}'

def edit_file(path , old , new , allow_multi_edit=False):
    with open(path) as f:
        content = f.read()

    # Counting how many times the `old` string
    # appears in content
    count = content.count(old)
    if count == 0:
        return f'Error: was not found in {path}'
    if count > 1 and not allow_multi_edit:
        return f'Error: {count} times in {path}, set `allow_multi_edit` to replace them all.'

    with open(path , 'w') as f:
        f.write(content.replace(old , new))
    
    return f'Replaced {count} match(es) in {path}'


TOOL_SCHEMAS = [
    {
        'type': 'function',
        'function': {
            'name': 'bash',
            'description': 'Run a shell command and return its combined stdout and stderr',
            'parameters': {
                'type': 'object',
                'properties': {
                    'command': {
                        'type': 'string',
                        'description': 'The shell command to run'
                    }
                },
                'required': ['command'],
            },
        },
    },
]

TOOLS = {
    'bash': bash,
    'read_file': read_file,
    'write_file': write_file,
    'edit_file': edit_file
}