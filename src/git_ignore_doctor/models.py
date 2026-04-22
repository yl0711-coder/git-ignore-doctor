from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RiskMatch:
    path: str
    category: str
    reason: str
    suggested_ignore: str | None = None


@dataclass(frozen=True)
class Report:
    root: str
    tracked_ignored: list[str] = field(default_factory=list)
    risky_tracked: list[RiskMatch] = field(default_factory=list)
    risky_untracked: list[RiskMatch] = field(default_factory=list)
    suggested_ignores: list[str] = field(default_factory=list)
    fix_plan: list[str] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return bool(
            self.tracked_ignored
            or self.risky_tracked
            or self.risky_untracked
            or self.suggested_ignores
        )

