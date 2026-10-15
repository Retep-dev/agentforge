import os
import sys
import unittest
from daily import allowed_path, run, select_task, tasks


class DailyTests(unittest.TestCase):
    def test_roadmap_has_ninety_ordered_tasks(self):
        self.assertEqual([number for number, _ in tasks()], list(range(1, 91)))

    def test_one_first_unfinished_task(self):
        self.assertEqual(select_task({"completed": [{"id": 1}]}), tasks()[1])

    def test_edit_scope(self):
        self.assertTrue(allowed_path("docs/architecture.md"))
        for path in ("../.env", ".github/workflows/daily.yml", "docs/../../.env", "backend/app/key.pem"):
            self.assertFalse(allowed_path(path))

    def test_untrusted_checks_do_not_receive_tokens(self):
        os.environ["OPENAI_API_KEY"] = "test-only-value"
        try:
            result = run(sys.executable, "-c", "import os; print(os.getenv('OPENAI_API_KEY', 'absent'))", untrusted=True)
            self.assertEqual(result.stdout.strip(), "absent")
        finally:
            os.environ.pop("OPENAI_API_KEY")


if __name__ == "__main__":
    unittest.main()
