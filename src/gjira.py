#!/usr/bin/env python3

from jira import JIRA
import os
import pathlib
import argparse
import subprocess


DEFAULT_MSG = "Jira issue: {}\nJira story {}"


def get_branch_name():
    return subprocess.check_output(
        ("git", "rev-parse", "--abbrev-ref", "HEAD",),
    ).decode("UTF-8")


def arg_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("--format", default=DEFAULT_MSG)
    parser.add_argument("--board")
    return parser.parse_args(argv)


def get_jira_from_env() -> dict:
    return {
        "server": os.environ.get("jiraserver"),
        "basic_auth": (os.environ.get("jirauser"), os.environ.get("jiratoken")),
    }


def get_jira_board() -> dict:
    cwd = pathlib.Path("../").parent.absolute()
    with open(pathlib.Path(cwd).joinpath(".jira")) as f:
        return f.readline().strip("\n")


def get_issue(jira: JIRA, id: str):
    return jira.issue(id)


def main():
    args = arg_parser(argv)

    options = get_jira_from_env()
    jira = JIRA(**options)
    board = get_jira_board()
    print(jira)
    print(board)


if __name__ == "__main__":
    main()
