import unittest

from git_ignore_doctor.rules import DEFAULT_RULES


class RiskRuleTest(unittest.TestCase):
    def test_detects_env_files_but_allows_example(self) -> None:
        env_rule = DEFAULT_RULES[0]

        self.assertTrue(env_rule.matches(".env"))
        self.assertFalse(env_rule.matches(".env.example"))

    def test_detects_nested_dependency_paths(self) -> None:
        vendor_rule = next(rule for rule in DEFAULT_RULES if rule.pattern == "vendor/*")

        self.assertTrue(vendor_rule.matches("vendor/autoload.php"))
        self.assertFalse(vendor_rule.matches("src/vendorish/file.php"))


if __name__ == "__main__":
    unittest.main()

