# Git Ignore Doctor

[English](README.md) | [简体中文](README.zh-CN.md)

A small CLI that tells you what your `.gitignore` forgot, and what Git is still tracking by mistake.

## Why

Many developers add a file to `.gitignore` and expect Git to stop tracking it. Git does not work that way: ignore rules only apply to untracked files. If a file has already been committed, it must be explicitly removed from the index.

Git Ignore Doctor turns that common confusion into a simple repository health report.

## Status

Current version: `v0.1.0`

The first version is intentionally small:

- no network access
- no background service
- no automatic cleanup
- no repository mutation
- no third-party runtime dependency

It is ready for local repository checks and CI reporting, but it should still be reviewed before being used as a hard blocking gate in large repositories.

## What It Checks

- Tracked files that already match ignore rules
- Risky tracked files such as `.env`, private keys, dependency folders, caches, build output, and logs
- Risky untracked files that may need `.gitignore` entries
- Suggested `.gitignore` entries
- Safe `git rm --cached` commands you can review before running

The tool does not modify your repository.

## Requirements

- Python 3.9 or later
- Git available in `PATH`
- A Git working tree

The CLI uses Git itself for ignored-file detection. It does not try to reimplement the full `.gitignore` specification.

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

GitHub Actions example:

```yaml
- name: Check repository hygiene
  run: bin/git-ignore-doctor --strict
```

JSON output is useful if you want to build a custom report:

```bash
bin/git-ignore-doctor --json > git-ignore-report.json
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

## Detection Scope

Git Ignore Doctor checks common repository hygiene risks:

- environment files: `.env`, `.env.*`
- private keys: `*.pem`, `*.key`, `id_rsa`, `id_ed25519`
- OS metadata: `.DS_Store`, `Thumbs.db`
- dependency directories: `vendor/`, `node_modules/`, `.venv/`, `venv/`
- caches: `__pycache__/`, `.pytest_cache/`, `.phpunit.cache/`
- build output: `coverage/`, `build/`, `dist/`, `.next/`
- logs: `*.log`

Allowed examples such as `.env.example` are not reported as risky.

## Non-Goals

Git Ignore Doctor does not try to be:

- a `.gitignore` template generator
- a secret scanner
- a full security audit tool
- an automatic cleanup tool
- a replacement for code review before removing files from Git

## Documentation Maintenance

When the English README changes, update `README.zh-CN.md` in the same pull request. The two README files should describe the same features, usage, and limitations.

## Development

```bash
PYTHONPATH=src python -m unittest discover -s tests
bin/git-ignore-doctor --strict
```

## License

MIT
