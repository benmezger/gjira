import os
import sys


def write_error(msg, file=sys.stderr, with_env=False):
    if with_env:
        print(
            f"Error: {msg}\n"
            + f"server: '{os.environ.get('jiraserver')}'\n"
            + f"email: '{os.environ.get('jirauser')}'\n"
            + f"token: '{os.environ.get('jiratoken')}'\n",
            file=file,
        )
        return

    print(f"Error: {msg}")
