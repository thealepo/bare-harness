import json
import subprocess


def bash(command):
    result = subprocess.run(command , shell=True , capture_output=True , text=True)
    return result.stdout + result.stderr

def read_file(path):
    pass

def write_file(path , content):
    pass

def edit_file(path , old , new , allow_multi_edit=False):
    pass


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