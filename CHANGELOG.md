<a name="v3.0.0"></a>
## [v3.0.0] - 2020-06-01

<a name="v3.1.0"></a>
## [v3.1.0] - 2020-06-07
### Feat
- Add HTTP max-retries flag and custom print
- Add CHANGELOG to project


<a name="v3.0.0"></a>
## [v3.0.0] - 2020-06-01
### Chore
- Update branch-check regex
- Enable pre-commit gjira's branch validation hook
- Lock Jira to version 2
- Add click as setup requirements

### Docs
- Update README with pre-push guide

### Feat
- Update commands
- Add commands test
- Add main test
- Add git tests
- Update click options
- Validate branch name
- Remove argparser and use click instead

### Fix
- Don't match regex, use findall instead

### Refactor
- Rename click commands
- Move click commands to commands.py
- Move git related code to git.py

### Pull Requests
- Merge pull request [#4](https://github.com/benmezger/gjira/issues/4) from benmezger/feat/click-and-check-branch-name


<a name="v2.2.8"></a>
## [v2.2.8] - 2020-06-01
### Docs
- Update README's example commit template

### Feat
- Add support to Jira bot

### Fix
- Don't match regex

### Pull Requests
- Merge pull request [#3](https://github.com/benmezger/gjira/issues/3) from fredericojordan/fred/jirabot


<a name="v2.2.7"></a>
## [v2.2.7] - 2020-05-24
### Docs
- Update demo section with asciicast and gif


<a name="v2.2.6"></a>
## [v2.2.6] - 2020-05-24
### Docs
- Add CI status to README


<a name="v2.2.5"></a>
## [v2.2.5] - 2020-05-24
### Feat
- Add coverate to tests
- Update test coverage on gjira module


<a name="v2.2.4"></a>
## [v2.2.4] - 2020-05-24
### Chore
- Add initial CircleCI config

### Fix
- Update broken tests on commit message


<a name="v2.2.3"></a>
## [v2.2.3] - 2020-05-23
### Fix
- Add branch issue regex to pre-commit-config
- Don't slice lines before writing to file


<a name="v2.2.2"></a>
## [v2.2.2] - 2020-05-23
### Fix
- Don't reappend lines


<a name="v2.2.1"></a>
## [v2.2.1] - 2020-05-23
### Fix
- Handle git commit -m


<a name="v2.2.0"></a>
## [v2.2.0] - 2020-05-23
### Feat
- Split diff type on pytest error
- Check Jira's inner attributes

### Refactor
- Move tests to project root


<a name="v2.0.0"></a>
## [v2.0.0] - 2020-05-22
### Build
- Use HEAD as revision for pre-commit
- Add Jinja2 requirement

### Docs
- Reformat README
- Add regex to docs
- Update README with new commit template

### Feat
- Add on empty commit message update
- Update README
- Add regex support for branching issues
- Add GJira mark to know where to stop reading
- Read and parse commit template
- Specify Python version

### Fix
- Add missing -- to template argument
- Add python requirement into single quotes

### Refactor
- Remove unused .jira file


<a name="v1.0.0"></a>
## v1.0.0 - 2020-05-18
### Build
- Update/add python requirements

### Docs
- Add asciinema
- Update README.md with development and TODOs
- fix readme typos
- Add initial readme

### Feat
- Catch error when fetching Jira issue
- Only get key and parent Jira fields
- Exit with 0 if branch in format
- Add initial tests
- Update git commit message by appending the ID
- Parse shell arguments when called
- Get current Git branch by spawning a Git process
- First commit. Get boards and issues by ID

### Fix
- Update Python version support
- Run on prepare-commit-msg

### Refactor
- Properly handle new lines in commit msg
- Change 'bad branch' error message
- Check branch before requesting Jira
- Rewrite whole file instead
- Move file to a package
- Use commit-msg as pre-commit stage

### Style
- Add typing to missing functions
- Reorder imports


[Unreleased]: https://github.com/benmezger/gjira/compare/v3.0.0...HEAD
[v3.0.0]: https://github.com/benmezger/gjira/compare/v2.2.8...v3.0.0
[v2.2.8]: https://github.com/benmezger/gjira/compare/v2.2.7...v2.2.8
[v2.2.7]: https://github.com/benmezger/gjira/compare/v2.2.6...v2.2.7
[v2.2.6]: https://github.com/benmezger/gjira/compare/v2.2.5...v2.2.6
[v2.2.5]: https://github.com/benmezger/gjira/compare/v2.2.4...v2.2.5
[v2.2.4]: https://github.com/benmezger/gjira/compare/v2.2.3...v2.2.4
[v2.2.3]: https://github.com/benmezger/gjira/compare/v2.2.2...v2.2.3
[v2.2.2]: https://github.com/benmezger/gjira/compare/v2.2.1...v2.2.2
[v2.2.1]: https://github.com/benmezger/gjira/compare/v2.2.0...v2.2.1
[v2.2.0]: https://github.com/benmezger/gjira/compare/v2.0.0...v2.2.0
[v2.0.0]: https://github.com/benmezger/gjira/compare/v1.0.0...v2.0.0
