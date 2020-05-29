import pytest

from jira import JIRA
import random


@pytest.fixture
def jira_connection(mocker):
    requests_get_mock = mocker.patch("requests.sessions.Session.get")
    requests_get_mock.return_value.status_code = 200
    requests_post_mock = mocker.patch("requests.sessions.Session.post")
    requests_post_mock.return_value.status_code = 201

    return JIRA(server="https://localhost", basic_auth=("me@benmezger.nl", "token"))


@pytest.fixture
def jira_attributes():
    return (
        "key",
        "parent.key",
        "summary",
        "parent.summary",
        "issuetype",
        "votes.votes",
    )


@pytest.fixture
def jira_issue(mocker):
    requests_get_mock = mocker.patch("requests.get")
    jira_get_issue_mock = mocker.patch("jira.JIRA.issue")

    issue = mocker.Mock(spec=("fields", "key"))

    issue.key = "ISSUE KEY"
    issue.fields.parent.key = "PARENT KEY"
    issue.fields.summary = "ISSUE SUMMARY"
    issue.fields.parent.summary = "PARENT SUMMARY"
    issue.fields.issuetype = "ISSUE TYPES"
    issue.fields.votes.votes = "ISSUE VOTES 4"

    jira_get_issue_mock.return_value = lambda: issue

    return issue


@pytest.fixture
def git_branch(mocker):
    def _mock_branch(branch=None):
        if branch is None:
            branch = "master"

        subprocess = mocker.patch("subprocess.check_output")
        subprocess.return_value = bytes(f"{branch}".encode("UTF-8"))
        return subprocess

    return _mock_branch
