from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


class GitRepository:
    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd
        self.root = self._find_root()

    def tracked_files(self) -> list[str]:
        return self._git_lines(["ls-files", "-z"], null_separated=True)

    def untracked_files(self) -> list[str]:
        return self._git_lines(["ls-files", "--others", "--exclude-standard", "-z"], null_separated=True)

    def tracked_ignored_files(self) -> list[str]:
        return self._git_lines(["ls-files", "-ci", "--exclude-standard", "-z"], null_separated=True)

    def _find_root(self) -> Path:
        output = self._run(["rev-parse", "--show-toplevel"], self.cwd)
        return Path(output.strip())

    def _git_lines(self, args: list[str], null_separated: bool = False) -> list[str]:
        output = self._run(args, self.root)

        if null_separated:
            return sorted(item for item in output.split("\0") if item)

        return sorted(line for line in output.splitlines() if line)

    @staticmethod
    def _run(args: list[str], cwd: Path) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if completed.returncode != 0:
            message = completed.stderr.strip() or completed.stdout.strip()
            raise GitError(message or "git command failed")

        return completed.stdout

