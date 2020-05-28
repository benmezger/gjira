#!/usr/bin/env python3

import pathlib
import sys
import re
import click

from jira import JIRA

from gjira.template import generate_template, get_template_context

from .gjira import (
    get_branch_name,
    get_issue,
    get_jira_from_env,
    is_gjira_in_file,
    update_commit_message,
)


def get_branch_id(regex):
    compiled_re = re.compile(regex)
    branch = get_branch_name()

    if not compiled_re.match(branch):
        print(f"Bad branch name. Expected format of '{regex}'. Skipping.")
        sys.exit(0)

    return compiled_re.findall(branch)[0]


@click.command()
@click.option("--board", "-b", required=True, type=str)
@click.option("--regex", "-r", required=True, type=str)
@click.option(
    "--template",
    "-t",
    type=click.Path(exists=True, writable=True, readable=True, resolve_path=True),
    default=str(pathlib.Path(".").joinpath(".commit.template")),
)
@click.argument("filename")
def update_commit_msg(filename: str, board: str, regex: str, template: str):
    if is_gjira_in_file(filename):
        print("Duplicated. Skipping")
        sys.exit(0)

    task_id = get_branch_id(regex)
    options = get_jira_from_env()

    jira = JIRA(**options)

    attributes = get_template_context(template)
    issue = get_issue(jira, task_id, attributes)

    if not issue.keys() or not issue.values():
        sys.exit(0)

    content = generate_template(issue, args.template)
    update_commit_message(args.filenames[0], content)


def main(argv=None):
    update_commit_msg()


if __name__ == "__main__":
    sys.exit(main())
