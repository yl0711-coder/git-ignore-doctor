from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .git import GitError, GitRepository
from .render import JsonRenderer, TextRenderer
from .scanner import Scanner


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="git-ignore-doctor",
        description="Diagnose tracked ignored files, risky commits, and missing .gitignore rules.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path inside the Git repository to inspect. Defaults to current directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Render the report as JSON.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when any issue is found.",
    )

    args = parser.parse_args(argv)

    try:
        repository = GitRepository(Path(args.path).resolve())
        report = Scanner(repository).scan()
    except GitError as error:
        print(f"git-ignore-doctor: {error}", file=sys.stderr)
        return 2

    renderer = JsonRenderer() if args.json else TextRenderer()
    print(renderer.render(report), end="")

    if args.strict and report.has_issues:
        return 1

    return 0

