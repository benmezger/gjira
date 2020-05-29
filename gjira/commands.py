import pathlib
import sys
import click

from jira import JIRA
from gjira.template import generate_template, get_template_context

from .gjira import (
    get_issue,
    get_jira_from_env,
    is_gjira_in_file,
    update_commit_message,
)

from .git import get_branch_id, get_branch_name, validate_branch_name


@click.command("append-jira")
@click.option("--board", "-b", required=True, type=str)
@click.option("--regex", "-r", required=True, type=str)
@click.option(
    "--template",
    "-t",
    type=click.Path(exists=True, writable=True, readable=True, resolve_path=True),
    default=str(pathlib.Path(".").joinpath(".commit.template")),
)
@click.argument("filename")
def cmd_update_commit_msg(filename: str, board: str, regex: str, template: str):
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

    content = generate_template(issue, template)
    update_commit_message(filename, content)


@click.command("check-branch")
@click.option(
    "--regex",
    "-r",
    required=True,
    type=str,
    help="Regex of a branch format to validate",
)
@click.option("--branch", "-b", type=str)
def cmd_validate_branch_name(branch_fmt: str, branch_name: str):
    if branch_name is None:
        branch_name = get_branch_name()

    valid = validate_branch_name(branch_name, branch_fmt)
    if valid is None:
        print(f"Branch name requires the format of '{branch_fmt}'. Aborting.")
        sys.exit(1)

    sys.exit(0)


@click.group()
def cli():
    pass


cli.add_command(cmd_validate_branch_name)
cli.add_command(cmd_update_commit_msg)
