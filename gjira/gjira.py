#!/usr/bin/env python3

import io
import os
import pathlib
import subprocess
import sys
from typing import Iterable

from jira import JIRA, Issue
from jira.exceptions import JIRAError

from gjira.output import write_error

GJIRA_START_TEXT = "Jira information:"
GIT_START_LINES = "# Please enter the commit message for your changes. Lines starting\n"


def get_jira_from_env() -> dict:
    return {
        "server": os.environ["jiraserver"],
        "basic_auth": (os.environ["jirauser"], os.environ["jiratoken"]),
    }


def issue_attr(
    prop: object,
    attribute: str,
    _from: str = "fields",
    attr_sep: str = ".",
    default=None,
):

    if hasattr(prop, attribute):
        return getattr(prop, attribute)

    tmp = getattr(prop, _from, None)
    for attr in attribute.split(attr_sep):
        tmp = getattr(tmp, attr, default)
    return tmp


def get_issue(jira: JIRA, id: str, attributes: Iterable) -> dict:
    try:
        issue = jira.issue(
            id, fields=", ".join(attr.split(".")[0] for attr in attributes)
        )
        return {
            k.replace(".", "__"): v
            for (k, v) in ((i, issue_attr(issue, i)) for i in attributes)
        }
    except JIRAError as e:
        if e.status_code == 404:
            write_error(f"Issue '{id}' not found.")
        else:
            write_error(
                f"Error fetching issue '{id}'. Status code: '{e.status_code}' | {e.msg}"
            )
        return {}


def is_gjira_in_file(path: str) -> bool:
    with open(path) as fd:
        for line in fd:
            if line.strip() == GJIRA_START_TEXT:
                return True
        return False


def update_commit_message(filename: str, content: str) -> list:
    if not content:
        return

    with open(filename, "r+") as fd:
        pos = 0
        lines = []
        for i, line in enumerate(fd):
            lines.append(line)
            # have we found where git default msg starts?
            if line == GIT_START_LINES:
                pos = i  # line number of git's default message
                break

        content = f"{GJIRA_START_TEXT}\n{content}\n"
        pos = pos if pos else -1

        if len(lines) > 1:
            if lines[pos - 1 if pos else 0].count("\n") > 1:
                content = f"{content}\n"
            else:
                content = f"\n{content}\n"
        else:
            content = f"\n{content}\n"

        # add fmt to the corresponding position and read any unread line
        lines = lines + [content] + fd.readlines()

        # Write lines back to file
        fd.seek(0)
        for line in lines:
            fd.write(line)

        return lines
