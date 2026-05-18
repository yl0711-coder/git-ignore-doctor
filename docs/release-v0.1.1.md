# Git Ignore Doctor v0.1.1

This maintenance release improves CI and repository audit usage.

## Added

- Added `--tracked-only` mode for checks that should ignore local untracked files.
- Documented when to use full local checks versus tracked-only checks.

## Fixed

- Updated `git_ignore_doctor.__version__` to `0.1.1` so runtime metadata matches the package version and release tag.

## Validation

- Unit tests passed.
- Source compilation passed.
- CLI import/version check passed.
