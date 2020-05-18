#!/usr/bin/env python3

import io
import os
import pathlib
import subprocess
import sys
from typing import Iterable

from jira import JIRA
from jira.exceptions import JIRAError


def extract_content_keys(content: str) -> dict:
    pass


def get_branch_name() -> str:
    return subprocess.check_output(("git", "rev-parse", "--abbrev-ref", "HEAD")).decode(
        "UTF-8"
    )


def get_jira_from_env() -> dict:
    return {
        "server": os.environ.get("jiraserver"),
        "basic_auth": (os.environ.get("jirauser"), os.environ.get("jiratoken")),
    }


def get_issue(jira: JIRA, id: str, attributes: Iterable) -> dict:
    try:
        issue = jira.issue(id, fields=", ".join(attributes))
        import pdb

        pdb.set_trace()
        return {k: v for (k, v) in ((i, getattr(issue, i, None)) for i in attributes)}
    except JIRAError as e:
        if e.status_code == 404:
            print(f"Issue '{id}' not found. Skipping.")
        else:
            print(
                f"Error fetching issue '{id}'. Status code: {e.status_code} | {e.msg}"
            )
        return {}


def update_commit_message(filename: str, fmt: str) -> list:
    with open(filename, "r+") as fd:
        pos = 0
        lines = []
        for i, line in enumerate(fd):
            lines.append(line)
            if line.startswith("#") and not pos:  # have we already found a #?
                pos = i
                break

        if len(lines) > 1:
            if lines[pos - 1].count("\n") > 1:
                fmt = f"{fmt}\n"
            else:
                fmt = f"\n{fmt}\n"
        else:
            fmt = f"\n{fmt}\n"

        # add fmt to the corresponding position and read any unread line
        lines = lines[:pos] + [fmt] + lines[pos:] + fd.readlines()

        # Write lines back to file
        fd.seek(0)
        for line in lines:
            fd.write(line)

        return lines
