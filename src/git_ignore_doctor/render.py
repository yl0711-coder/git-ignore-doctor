from __future__ import annotations

import json

from .models import Report, RiskMatch


class TextRenderer:
    def render(self, report: Report) -> str:
        lines: list[str] = [
            "Git Ignore Doctor",
            "",
            f"Repository: {report.root}",
            "",
        ]

        self._section(lines, "Tracked files that match ignore rules", report.tracked_ignored)
        self._risk_section(lines, "Risky tracked files", report.risky_tracked)
        self._risk_section(lines, "Risky untracked files", report.risky_untracked)
        self._section(lines, "Suggested .gitignore entries", report.suggested_ignores)
        self._section(lines, "Suggested safe commands", report.fix_plan)

        lines.append("Result: failed" if report.has_issues else "Result: clean")

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _section(lines: list[str], title: str, items: list[str]) -> None:
        lines.append(f"{title}:")

        if not items:
            lines.append("- none")
            lines.append("")
            return

        for item in items:
            lines.append(f"- {item}")

        lines.append("")

    @staticmethod
    def _risk_section(lines: list[str], title: str, items: list[RiskMatch]) -> None:
        lines.append(f"{title}:")

        if not items:
            lines.append("- none")
            lines.append("")
            return

        for item in items:
            lines.append(f"- {item.path} [{item.category}] {item.reason}")

        lines.append("")


class JsonRenderer:
    def render(self, report: Report) -> str:
        payload = {
            "repository": report.root,
            "tracked_ignored": report.tracked_ignored,
            "risky_tracked": [risk_to_dict(item) for item in report.risky_tracked],
            "risky_untracked": [risk_to_dict(item) for item in report.risky_untracked],
            "suggested_ignores": report.suggested_ignores,
            "fix_plan": report.fix_plan,
            "has_issues": report.has_issues,
        }

        return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def risk_to_dict(item: RiskMatch) -> dict[str, str | None]:
    return {
        "path": item.path,
        "category": item.category,
        "reason": item.reason,
        "suggested_ignore": item.suggested_ignore,
    }

