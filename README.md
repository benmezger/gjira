[![CircleCI](https://circleci.com/gh/benmezger/gjira.svg?style=svg)](https://circleci.com/gh/benmezger/gjira)

# GJira

GJira fetches a Jira issue based on the current branch name and appends to the
commit body.

GJira allows dynamic branches to be set per project and commit template by using
dynamic Jira attributes.

## Why?

This came as a requirement from projects I work where makes heavy use of Jira.
Jira has support for [Smart
commits](https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html)
which we use in all projects where I work. This allows us to dynamically move
cards around depending on their status, and link commits and branches to them.

It's a neat feature for developers and projects managers, as it removes the
overhead from developers by having to move cards around manually on each push
and gives the project manager an insight of the current development workload.

## Requirements

- Python >=3
- [pre-commit](https://pre-commit.com/)

## Setup

### Git commit template

GJira requires a commit template file. GJira supports Jinja2, which allows
customizable templates based on Jira context. For example:

```text
# The following is automatically by 'commit.template'

Jira issue: [{{ key }}]
{% if parent__key %}{Jira story: [{{ parent__key }}]}{% endif %}
{% if summary %}{Jira summary: {{ summary }}}{% endif %}
```

The keys are related to Jira issue attributes. For example:

```text
issue.fields.worklog.worklogs[0].author
issue.fields.worklog.worklogs[0].comment
issue.fields.worklog.worklogs[0].created
issue.fields.worklog.worklogs[0].id
issue.fields.worklog.worklogs[0].self
issue.fields.worklog.worklogs[0].started
issue.fields.worklog.worklogs[0].timeSpent
issue.fields.worklog.worklogs[0].timeSpentSeconds
issue.fields.worklog.worklogs[0].updateAuthor                # dictionary
issue.fields.worklog.worklogs[0].updated

issue.fields.timetracking.remainingEstimate           # may be NULL or string ("0m", "2h"...)
issue.fields.timetracking.remainingEstimateSeconds    # may be NULL or integer
issue.fields.timetracking.timeSpent                   # may be NULL or string
issue.fields.timetracking.timeSpentSeconds            # may be NULL or integer
```

Inner issue fields **require** `.` (dot) to be replaced with `__` (double
underscore).

### Branch

GJira find Jira ID by the branch name. You can use a regex to specify the
location for the issue ID, for example: the regex `ISSUE-\d+` will match
`ISSUE-123/branch-name` or `ISSUE-123-branch-name` etc.

### pre-commit

Add the following repository to your `.pre-commit-config.yml` file

```yaml
- repo: https://github.com/benmezger/gjira
  rev: master
  hooks:
    - id: gjira
      args: ["--board=<board/project name>",
            "--template=.commit.template",
            "--regex='ISSUE-\d+'"]
```

### Environment variables

Set the following environment variables:

```sh
export jiraserver="https://domain.atlassian.net"
export jirauser="your@email.com"

# from: https://id.atlassian.com/manage-profile/security/api-tokens
export jiratoken="token"
```

### Installing the hook

Finally, install the hook with pre-commit: `pre-commit install --hook-type prepare-commit-msg`.

## Demo

### Using Git in the terminal

[![asciicast](https://asciinema.org/a/GGURgGibHGHII9jaIH5a5w3Yq.svg)](https://asciinema.org/a/GGURgGibHGHII9jaIH5a5w3Yq)

### Using Git in VSCode

![GJira VScode](images/vscode.gif)

## Troubleshooting

- GJira is not appending the issue/story to the commit message.

  That's probably because you are not checkout to a branch with the required
  format or credentials are possibly wrong.

- GJira is not appending the story ID

  That's probably because your issue is not a subtask of a story.

- I need it solved right now!

  Run `pre-commit uninstall --hook-type prepare-commit-msg`. That should disable
  `prepare-commit-msg`.

## Development

1. Install requirements `pip install -r requirements.txt`
2. Run `pytest` `pytest .`

There are two ways of manually running GJira.

1. `python -m gjira` which will run `main()` in `__main__`
2. Installing the cli to your system `pip install .`

## TODO

- Cache issues the board and check the cache before doing a HTTP request
  - add `--refresh` parameter to GJira
