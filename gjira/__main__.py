#!/usr/bin/env python3

import argparse
import pathlib
import sys

from jira import JIRA

from gjira.template import generate_template, get_template_context

from .gjira import get_branch_name, get_issue, get_jira_from_env, update_commit_message


def arg_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument(
        "template",
        default=str(pathlib.Path(".").joinpath(".commit.template")),
        nargs="?",
    )
    parser.add_argument("--board")
    return parser.parse_args(argv)


def get_branch_id():
    branch = get_branch_name().split("/")

    if len(branch) == 1:
        print("Bad branch name. Expected format of <id>/<txt>. Skipping.")
        sys.exit(0)

    return branch[0]


def main(argv=None):
    args = arg_parser(argv)

    task_id = get_branch_id()
    options = get_jira_from_env()

    jira = JIRA(**options)

    attributes = get_template_context(args.template)
    issue = get_issue(jira, task_id, attributes)
    content = generate_template(issue, args.template)

    update_commit_message(args.filenames[0], content)


if __name__ == "__main__":
    sys.exit(main())
