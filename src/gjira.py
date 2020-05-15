#!/usr/bin/env python3

from jira import JIRA
import os
import pathlib


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
    options = get_jira_from_env()
    jira = JIRA(**options)
    board = get_jira_board()
    print(jira)
    print(board)


if __name__ == "__main__":
    main()
