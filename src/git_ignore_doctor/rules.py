from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch


@dataclass(frozen=True)
class RiskRule:
    pattern: str
    category: str
    reason: str
    suggested_ignore: str | None = None
    allow: tuple[str, ...] = ()

    def matches(self, path: str) -> bool:
        normalized = normalize_path(path)

        if normalized in self.allow or any(fnmatch(normalized, item) for item in self.allow):
            return False

        return (
            fnmatch(normalized, self.pattern)
            or fnmatch("/" + normalized, self.pattern)
            or any(fnmatch(part, self.pattern) for part in normalized.split("/"))
        )


DEFAULT_RULES: tuple[RiskRule, ...] = (
    RiskRule(".env", "secret", "Environment files often contain credentials.", ".env", allow=(".env.example",)),
    RiskRule(".env.*", "secret", "Environment variants often contain local credentials.", ".env.*", allow=(".env.example", ".env.*.example")),
    RiskRule("*.pem", "secret", "PEM private keys should not be committed.", "*.pem"),
    RiskRule("*.key", "secret", "Private key files should not be committed.", "*.key"),
    RiskRule("id_rsa", "secret", "SSH private keys should not be committed.", "id_rsa"),
    RiskRule("id_ed25519", "secret", "SSH private keys should not be committed.", "id_ed25519"),
    RiskRule(".DS_Store", "os", "macOS metadata files add noise to repositories.", ".DS_Store"),
    RiskRule("Thumbs.db", "os", "Windows thumbnail cache files add noise to repositories.", "Thumbs.db"),
    RiskRule("vendor/*", "dependency", "PHP Composer dependencies are usually installed, not committed.", "/vendor/"),
    RiskRule("node_modules/*", "dependency", "Node dependencies are usually installed, not committed.", "/node_modules/"),
    RiskRule(".venv/*", "dependency", "Python virtual environments should not be committed.", "/.venv/"),
    RiskRule("venv/*", "dependency", "Python virtual environments should not be committed.", "/venv/"),
    RiskRule("__pycache__/*", "cache", "Python bytecode cache should not be committed.", "__pycache__/"),
    RiskRule(".pytest_cache/*", "cache", "Pytest cache should not be committed.", "/.pytest_cache/"),
    RiskRule(".phpunit.cache/*", "cache", "PHPUnit cache should not be committed.", "/.phpunit.cache/"),
    RiskRule("coverage/*", "build", "Coverage output should not be committed.", "/coverage/"),
    RiskRule("build/*", "build", "Build output is usually generated and should be ignored.", "/build/"),
    RiskRule("dist/*", "build", "Distribution output is usually generated and should be ignored.", "/dist/"),
    RiskRule(".next/*", "build", "Next.js build output should not be committed.", "/.next/"),
    RiskRule("*.log", "log", "Log files should not be committed.", "*.log"),
)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")

