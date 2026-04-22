from __future__ import annotations

from pathlib import Path

from .git import GitRepository
from .models import Report, RiskMatch
from .rules import DEFAULT_RULES, RiskRule, normalize_path


class Scanner:
    def __init__(self, repository: GitRepository, rules: tuple[RiskRule, ...] = DEFAULT_RULES) -> None:
        self.repository = repository
        self.rules = rules

    def scan(self) -> Report:
        tracked_files = self.repository.tracked_files()
        untracked_files = self.repository.untracked_files()
        tracked_ignored = self.repository.tracked_ignored_files()

        risky_tracked = self._risk_matches(tracked_files)
        risky_untracked = self._risk_matches(untracked_files)
        suggested_ignores = self._suggested_ignores(risky_tracked, risky_untracked, tracked_ignored)
        fix_plan = self._fix_plan(tracked_ignored, risky_tracked)

        return Report(
            root=str(self.repository.root),
            tracked_ignored=tracked_ignored,
            risky_tracked=risky_tracked,
            risky_untracked=risky_untracked,
            suggested_ignores=suggested_ignores,
            fix_plan=fix_plan,
        )

    def _risk_matches(self, paths: list[str]) -> list[RiskMatch]:
        matches: list[RiskMatch] = []
        seen: set[tuple[str, str]] = set()

        for path in paths:
            for rule in self.rules:
                if not rule.matches(path):
                    continue

                key = (path, rule.category)
                if key in seen:
                    continue

                matches.append(
                    RiskMatch(
                        path=normalize_path(path),
                        category=rule.category,
                        reason=rule.reason,
                        suggested_ignore=rule.suggested_ignore,
                    )
                )
                seen.add(key)

        return matches

    def _suggested_ignores(
        self,
        risky_tracked: list[RiskMatch],
        risky_untracked: list[RiskMatch],
        tracked_ignored: list[str],
    ) -> list[str]:
        ignore_entries = self._read_gitignore_entries()
        suggestions: set[str] = set()

        for match in [*risky_tracked, *risky_untracked]:
            if match.suggested_ignore and match.suggested_ignore not in ignore_entries:
                suggestions.add(match.suggested_ignore)

        for path in tracked_ignored:
            parent = self._directory_suggestion(path)
            if parent and parent not in ignore_entries:
                suggestions.add(parent)

        return sorted(suggestions)

    def _read_gitignore_entries(self) -> set[str]:
        gitignore = Path(self.repository.root) / ".gitignore"

        if not gitignore.exists():
            return set()

        entries: set[str] = set()
        for line in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                entries.add(stripped)

        return entries

    @staticmethod
    def _directory_suggestion(path: str) -> str | None:
        normalized = normalize_path(path)

        if "/" not in normalized:
            return None

        return "/" + normalized.split("/", 1)[0] + "/"

    @staticmethod
    def _fix_plan(tracked_ignored: list[str], risky_tracked: list[RiskMatch]) -> list[str]:
        paths = sorted({*tracked_ignored, *(match.path for match in risky_tracked)})

        return [f"git rm --cached -- {shell_quote(path)}" for path in paths]


def shell_quote(value: str) -> str:
    if value.replace("/", "").replace(".", "").replace("-", "").replace("_", "").isalnum():
        return value

    return "'" + value.replace("'", "'\"'\"'") + "'"

