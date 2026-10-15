import unittest
from daily import allowed_path, select_task, tasks


class DailyTests(unittest.TestCase):
    def test_roadmap_has_ninety_ordered_tasks(self):
        self.assertEqual([number for number, _ in tasks()], list(range(1, 91)))

    def test_one_first_unfinished_task(self):
        self.assertEqual(select_task({"completed": [{"id": 1}]}), tasks()[1])

    def test_edit_scope(self):
        self.assertTrue(allowed_path("docs/architecture.md"))
        for path in ("../.env", ".github/workflows/daily.yml", "docs/../../.env", "backend/app/key.pem"):
            self.assertFalse(allowed_path(path))


if __name__ == "__main__":
    unittest.main()
