import json
import subprocess


def bash(command):
    pass

def read_file(path):
    pass

def write_file(path , content):
    pass

def edit_file(path , old , new , allow_multi_edit=False):
    pass


TOOLS = {
    'bash': bash,
    'read_file': read_file,
    'write_file': write_file,
    'edit_file': edit_file
}