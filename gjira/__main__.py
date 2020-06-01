#!/usr/bin/env python3

import argparse
import pathlib
import sys
import re

from jira import JIRA

from gjira.template import generate_template, get_template_context

from .gjira import (
    get_branch_name,
    get_issue,
    get_jira_from_env,
    is_gjira_in_file,
    update_commit_message,
)


def arg_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument(
        "--template",
        default=str(pathlib.Path(".").joinpath(".commit.template")),
        nargs="?",
    )
    parser.add_argument("--board")
    parser.add_argument("--regex")
    return parser.parse_args(argv)


def get_branch_id(regex):
    compiled_re = re.compile(regex)
    branch = get_branch_name()

    if not compiled_re.findall(branch):
        print(f"Bad branch name. Expected format of '{regex}'. Skipping.")
        sys.exit(0)

    return compiled_re.findall(branch)[0]


def main(argv=None):
    args = arg_parser(argv)

    if is_gjira_in_file(args.filenames[0]):
        print("Duplicated. Skipping")
        sys.exit(0)

    task_id = get_branch_id(args.regex)
    options = get_jira_from_env()

    jira = JIRA(**options)

    attributes = get_template_context(args.template)
    issue = get_issue(jira, task_id, attributes)

    if not issue.keys() or not issue.values():
        sys.exit(0)

    content = generate_template(issue, args.template)
    update_commit_message(args.filenames[0], content)


if __name__ == "__main__":
    sys.exit(main())
