import unittest
from analytics import calculate_completion_rate

class TestAnalytics(unittest.TestCase):

    def test_calculate_completion_rate_empty_list(self):
        """
        Test that calculate_completion_rate returns 0.0 for an empty list.
        """
        tasks = []
        self.assertEqual(calculate_completion_rate(tasks), 0.0)

    def test_calculate_completion_rate_mixed_tasks(self):
        """
        Test calculate_completion_rate with a mix of pending and completed tasks.
        """
        tasks = [
            {"id": 1, "title": "Task 1", "status": "Completed"},
            {"id": 2, "title": "Task 2", "status": "Pending"},
            {"id": 3, "title": "Task 3", "status": "Completed"},
            {"id": 4, "title": "Task 4", "status": "Pending"},
            {"id": 5, "title": "Task 5", "status": "Pending"},
        ]
        # Expected: 2 completed out of 5 total = 40.0%
        self.assertEqual(calculate_completion_rate(tasks), 40.0)

    def test_calculate_completion_rate_all_completed(self):
        """
        Test calculate_completion_rate when all tasks are completed.
        """
        tasks = [
            {"id": 1, "title": "Task 1", "status": "Completed"},
            {"id": 2, "title": "Task 2", "status": "Completed"},
        ]
        self.assertEqual(calculate_completion_rate(tasks), 100.0)

    def test_calculate_completion_rate_all_pending(self):
        """
        Test calculate_completion_rate when all tasks are pending.
        """
        tasks = [
            {"id": 1, "title": "Task 1", "status": "Pending"},
            {"id": 2, "title": "Task 2", "status": "Pending"},
        ]
        self.assertEqual(calculate_completion_rate(tasks), 0.0)

if __name__ == '__main__':
    unittest.main()
