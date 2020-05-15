#!/usr/bin/env python3

from jira import JIRA
import os
import pathlib
import subprocess


DEFAULT_MSG = "Jira issue: {}\nJira story {}"


def get_branch_name():
    return subprocess.check_output(
        ("git", "rev-parse", "--abbrev-ref", "HEAD",),
    ).decode("UTF-8")


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
