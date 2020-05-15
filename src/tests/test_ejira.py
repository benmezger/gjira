import pytest
from .. import gjira
import os


def test_get_branch_name(mocker):
    subprocess = mocker.patch("subprocess.check_output")
    subprocess.return_value = b"SK12/feat/test"
    gjira.get_branch_name()
    assert subprocess.called_once_with("git", "rev-parse", "--abbrev-ref", "HEAD")


def test_get_jira_config(mocker):
    environ_mock = mocker.patch.dict(
        os.environ,
        {
            "jiraserver": "http://testserver.com",
            "jirauser": "test-user@test.com",
            "jiratoken": "172y1dsyd7asda",
        },
    )
    assert gjira.get_jira_from_env() == {
        "server": "http://testserver.com",
        "basic_auth": ("test-user@test.com", "172y1dsyd7asda",),
    }
