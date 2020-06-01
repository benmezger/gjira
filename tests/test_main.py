import pytest
from gjira.__main__ import main


def test_main(mocker):
    update_commit = mocker.patch("gjira.commands.cmd_update_commit_msg")
    validate_branch = mocker.patch("gjira.commands.cmd_validate_branch_name")
    with pytest.raises(SystemExit) as exc_info:
        main()

    assert update_commit.called_once()
    assert validate_branch.called_once()

    assert exc_info.type == SystemExit
    assert exc_info.value.code == 0
