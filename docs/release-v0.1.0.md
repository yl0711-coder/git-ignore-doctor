# v0.1.0

Initial public release of Git Ignore Doctor.

## Added

- CLI for detecting tracked files that already match `.gitignore`
- Detection for common risky tracked and untracked files such as `.env`, private keys, dependency directories, caches, build output, OS metadata, and logs
- Suggested `.gitignore` entries
- Safe `git rm --cached` fix plan output
- `--json` output for custom reporting
- `--strict` mode for CI usage
- English and Chinese README
- Demand research document based on recurring Git and Stack Overflow problems

## Verified

- Unit tests passed
- CLI self-check passed
- Dirty repository simulation detected `.env`, `.DS_Store`, and `vendor/autoload.php` correctly
- GitHub Actions workflow added for Python 3.9 to 3.12

## Positioning

Git Ignore Doctor is intentionally small. It does not generate generic `.gitignore` templates and does not auto-fix repositories. It focuses on diagnosing existing repositories and producing a human-reviewable fix plan.
