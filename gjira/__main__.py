import sys
from .commands import cmd_update_commit_msg, cmd_validate_branch_name, cli


def main(argv=None):
    cli()


if __name__ == "__main__":
    sys.exit(main())
