from click.testing import CliRunner
import pytest

from gjira.commands import cmd_update_commit_msg, cmd_validate_branch_name


def test_cmd_update_commit_msg(mocker, cli, git_branch, jira_connection, jira_issue):
    git_branch("SKYR-123")
    with cli.isolated_filesystem():
        with open(".commit.template", "w") as commitf:
            commitf.write("Jira issue: {{key}}\nJira story {{parent__key}}")

        with open("COMMIT_MSG", "w") as msgf:
            msgf.write("Feat: A commit message")

        result = cli.invoke(
            cmd_update_commit_msg,
            ["--regex", "SKYR-\d+", "--board", "boardname", "COMMIT_MSG"],
        )
        assert result.exit_code == 0
        assert result.output == ""
        assert result.exception == None


def test_cmd_update_commit_msg_with_ignored_file(
    mocker, cli, git_branch, jira_connection, jira_issue
):
    with cli.isolated_filesystem():
        with open(".commit.template", "w") as commitf:
            commitf.write("Jira issue: {{key}}\nJira story {{parent__key}}")

        with open("MERGE_MSG", "w") as msgf:
            msgf.write("Feat: A commit message")

        result = cli.invoke(
            cmd_update_commit_msg,
            ["--regex", "SKYR-\d+", "--board", "boardname", "MERGE_MSG"],
        )
        assert result.exit_code == 0
        assert result.output == "File 'MERGE_MSG'. Skipping.\n"
        assert result.exception == None
        assert result.exc_info[0] == SystemExit


def test_cmd_validate_branch_name_with_branch_specified(cli, git_branch):
    result = cli.invoke(
        cmd_validate_branch_name,
        ["--regex", "JIRA-\d+_[a-z]+(-[a-z]+)*$", "--branch", "JIRA-123_hello-world"],
    )
    assert result.exit_code == 0
    assert result.output == ""
    assert result.exception == None


def test_cmd_validate_branch_name_with_no_branch_specified(cli, git_branch):
    git_branch("JIRA-123_hello-world")
    result = cli.invoke(
        cmd_validate_branch_name, ["--regex", "JIRA-\d+_[a-z]+(-[a-z]+)*$"]
    )
    assert result.exit_code == 0
    assert result.output == ""
    assert result.exception == None


def test_cmd_validate_branch_name_with_invalid_name(cli):
    result = cli.invoke(
        cmd_validate_branch_name,
        [
            "--regex",
            "JIRA-\d+_[a-z]+(-[a-z]+)*$",
            "--branch",
            "JIRA-1234_hello_world-123",
        ],
    )
    assert result.exit_code == 1
    assert (
        result.output
        == "Branch name requires the format of 'JIRA-\\d+_[a-z]+(-[a-z]+)*$'. Aborting.\n"
    )
