#!/usr/bin/env python3

import sys
from jira import JIRA
from .gjira import (
    get_jira_from_env,
    get_branch_name,
    get_issue,
    get_issue_parent,
    update_commit_message,
    DEFAULT_MSG,
)

import argparse


def arg_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("--format", default=DEFAULT_MSG)
    parser.add_argument("--board")
    return parser.parse_args(argv)


def get_branch_id():
    branch = get_branch_name().split("/")

    if len(branch) == 1:
        print("Bad branch name. Expected format of <id>/<txt>")
        sys.exit(0)

    return branch[0]


def main(argv=None):
    args = arg_parser(argv)
    options = get_jira_from_env()
    jira = JIRA(**options)

    task_id = get_branch_id()

    # branch_issue = get_issue(jira, ticket_id)
    branch_issue = get_issue(jira, task_id)
    branch_story = get_issue_parent(branch_issue)

    fmt = (args.format or DEFAULT_MSG).format(branch_issue, branch_story)

    update_commit_message(args.filenames[0], fmt)


if __name__ == "__main__":
    sys.exit(main())
