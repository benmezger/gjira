import sys
from .commands import cmd_update_commit_msg


def main(argv=None):
    cmd_update_commit_msg()


if __name__ == "__main__":
    sys.exit(main())
