#!/usr/bin/env python3

from jira import JIRA
import os, sys
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


def get_issue(jira: JIRA, id: str):
    return jira.issue(id)


def get_issue_parent(issue) -> str:
    if hasattr(issue.fields, "parent"):
        return issue.fields.parent.key
    return ""


def update_commit_message(filename, fmt):
    with open(filename, "r+") as fd:
        contents = fd.readlines()
        if not contents:
            return

        if len(contents) > 1:
            fd.write(f"\n{fmt}")
            return
        fd.write(f"\n\n{fmt}")


def main(argv=None):
    args = arg_parser(argv)

    options = get_jira_from_env()
    jira = JIRA(**options)

    branch = get_branch_name().split("/")

    if len(branch) == 1:
        raise ValueError("Bad branch name. Expected format of <id>/<txt>")

    ticket_id = branch[0]

    # branch_issue = get_issue(jira, ticket_id)
    branch_issue = get_issue(jira, "SKYR-1990")
    branch_story = get_issue_parent(branch_issue)

    fmt = (args.format or DEFAULT_MSG).format(branch_issue, branch_story)

    update_commit_message(args.filenames[0], fmt)


if __name__ == "__main__":
    sys.exit(main())
