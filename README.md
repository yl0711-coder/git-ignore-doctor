# Git Ignore Doctor

A small CLI that tells you what your `.gitignore` forgot, and what Git is still tracking by mistake.

## Why

Many developers add a file to `.gitignore` and expect Git to stop tracking it. Git does not work that way: ignore rules only apply to untracked files. If a file has already been committed, it must be explicitly removed from the index.

Git Ignore Doctor turns that common confusion into a simple repository health report.

## What It Checks

- Tracked files that already match ignore rules
- Risky tracked files such as `.env`, private keys, dependency folders, caches, build output, and logs
- Risky untracked files that may need `.gitignore` entries
- Suggested `.gitignore` entries
- Safe `git rm --cached` commands you can review before running

The tool does not modify your repository.

## Usage

Run from any path inside a Git repository:

```bash
bin/git-ignore-doctor
```

Inspect another repository:

```bash
bin/git-ignore-doctor /path/to/repo
```

Use JSON output:

```bash
bin/git-ignore-doctor --json
```

Use strict mode for CI:

```bash
bin/git-ignore-doctor --strict
```

You can also install the package locally if your Python environment has packaging tools available:

```bash
python -m pip install -e .
git-ignore-doctor --strict
```

Exit codes:

- `0`: command ran successfully
- `1`: issues found in `--strict` mode
- `2`: invalid input or Git error

## Example Output

```text
Git Ignore Doctor

Repository: /work/my-app

Tracked files that match ignore rules:
- .DS_Store

Risky tracked files:
- .env [secret] Environment files often contain credentials.
- vendor/autoload.php [dependency] PHP Composer dependencies are usually installed, not committed.

Risky untracked files:
- debug.log [log] Log files should not be committed.

Suggested .gitignore entries:
- .env
- *.log
- /vendor/

Suggested safe commands:
- git rm --cached -- .DS_Store
- git rm --cached -- .env
- git rm --cached -- vendor/autoload.php

Result: failed
```

## Design Notes

Git Ignore Doctor intentionally reports a fix plan instead of changing your repository. Commands such as `git rm --cached` are safe when reviewed, but they still affect the Git index. The first version keeps humans in control.

See [docs/research.md](docs/research.md) for the demand research behind this tool.

## Development

```bash
PYTHONPATH=src python -m unittest discover -s tests
bin/git-ignore-doctor --strict
```

## License

MIT
