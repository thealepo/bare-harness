# TODO: WIP

import subprocess
from datetime import datetime

def git_branch():
    result = subprocess.run(
        'git branch --show-current' , shell=True , capture_output=True , text=True
    )
    return result.stdout.strip() or '(detached)'