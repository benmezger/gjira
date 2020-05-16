# GJira

GJira fetches a Jira issue based on the current branch name and appends to the
commit body.

The current supported branch format is `<issue_id>/<any/<text>`. GJira will
first check whether the branch starts with the expected format, if not, it
exits with `0` without exiting Git, otherwise it connects to Jira and gets the
task/story ID and appends to the body of the commit.

## Why?

This came as a requirement from projects I work, where the branch name is
required to have the task id, separated by a `/` and commits need to have the
issue id and story id attached. This allows managers to view commit flow during
the week and visually team performance.

## Requirements

- Python >=3
- [pre-commit](https://pre-commit.com/)

## Setup

Add the following repository to your `.pre-commit-config.yml` file

```yaml
- repo: https://github.com/benmezger/gjira
  rev: master
  hooks:
    - id: gjira
      args: ["--board=<board/project name>"]
```

Change `<board/projec name>` with your current Jira project. Finally, set the
following environment variables:

```sh
export jiraserver="https://domain.atlassian.net"
export jirauser="your@email.com"

# from: https://id.atlassian.com/manage-profile/security/api-tokens
export jiratoken="token"
```

Finally, install the hook with pre-commit: `pre-commit install --hook-type prepare-commit-msg`.

## Troubleshooting

- GJira is not appending the issue/story to the commit message.

  That's probably because you are not checkout to a branch with the required
  format or credentials are possibly wrong.

- GJira is not appending the story ID

  That's probably because your issue is not a subtask of a story.

- I need it solved right now!

  Run `pre-commit uninstall --hook-type prepare-commit-msg`. That should disable
  `prepare-commit-msg`.
