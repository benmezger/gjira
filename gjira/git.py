from typing import Union
import re
import subprocess
import sys


def get_branch_name() -> str:
    return subprocess.check_output(("git", "rev-parse", "--abbrev-ref", "HEAD")).decode(
        "UTF-8"
    )


def get_branch_id(regex):
    compiled_re = re.compile(regex)
    branch = get_branch_name()

    if not compiled_re.findall(branch):
        print(f"Bad branch name. Expected format of '{regex}'. Skipping.")
        sys.exit(0)

    return compiled_re.findall(branch)[0]


def validate_branch_name(branch: str, regex: str) -> Union[list, None]:
    compiled_re = re.compile(regex)
    if not compiled_re.match(branch):
        return None
    return compiled_re.findall(branch)
