import os

import pytest

from .. import gjira


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


def test_update_commit_msg_without_summary(mocker):
    file_text = """
    # A properly formed Git commit subject line should always be able to complete
    # the following sentence:
    #     * If applied, this commit <will your subject line here>
    #
    # [Add/Fix/Remove/Update/Refactor/Document/Style]: [issue #id] [summary]
    """

    fmt = "Jira issue: {ID-123}\nJira story {ID-456}"

    open_mock = mocker.patch("builtins.open", mocker.mock_open(read_data=file_text))

    gjira.update_commit_message("testfile", fmt)
    open_mock.assert_called_once_with("testfile", "r+")
    write = open_mock()

    assert f"\nJira information:\n{fmt}\n\n" == write.write.call_args_list[6].args[0]
    for (line, call) in zip(file_text.split("\n"), write.write.call_args_list[:6]):
        assert line.strip() in call.args[0].strip("\n")


def test_update_commit_msg_with_summary(mocker):
    file_text = """This is a summary and jira should be added in the next line after the comment.
    # A properly formed Git commit subject line should always be able to complete
    # the following sentence:
    #     * If applied, this commit <will your subject line here>
    #
    # [Add/Fix/Remove/Update/Refactor/Document/Style]: [issue #id] [summary]
    """

    fmt = "Jira issue: {ID-123}\nJira story {ID-456}"
    open_mock = mocker.patch("builtins.open", mocker.mock_open(read_data=file_text))

    gjira.update_commit_message("testfile", fmt)
    open_mock.assert_called_once_with("testfile", "r+")
    write = open_mock()

    assert f"\nJira information:\n{fmt}\n\n" == write.write.call_args_list[6].args[0]
    for (line, call) in zip(file_text.split("\n"), write.write.call_args_list[:6]):
        assert line.strip() in call.args[0].strip("\n")


def test_update_commit_msg_with_empty_text(mocker):
    file_text = ""
    fmt = "Jira issue: 123\nJira story: 1234"

    open_mock = mocker.patch("builtins.open", mocker.mock_open(read_data=file_text))

    gjira.update_commit_message("testfile", fmt)
    open_mock.assert_called_once_with("testfile", "r+")
    write = open_mock()

    assert f"\nJira information:\n{fmt}\n\n" == write.write.call_args_list[0].args[0]
    for (line, call) in zip(file_text.split("\n")[1:], write.write.call_args_list[2:]):
        assert line.strip() in call.args[0].strip("\n")


def test_update_commit_msg_with_empty_text(mocker):
    file_text = ""
    fmt = "Jira issue: 123\nJira story: 1234"

    open_mock = mocker.patch("builtins.open", mocker.mock_open(read_data=file_text))

    gjira.update_commit_message("testfile", fmt)
    open_mock.assert_called_once_with("testfile", "r+")
    write = open_mock()

    assert f"\nJira information:\n{fmt}\n\n" == write.write.call_args_list[0].args[0]
    for (line, call) in zip(file_text.split("\n")[1:], write.write.call_args_list[2:]):
        assert line.strip() in call.args[0].strip("\n")
