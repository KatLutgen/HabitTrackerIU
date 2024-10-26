import unittest
from datetime import datetime, timedelta
import tkinter as tk
from models.Habit import Habit
from models.HabitRecord import HabitRecord
from database.db_manager import DBManager
from analytics.AnalyticsInterface import AnalyticsInterface

class TestHabitManagement(unittest.TestCase):
    def setUp(self):
        self.db_manager = DBManager()
        self.db_manager.initialize_database()
        self.habit = Habit(
            name="Read",
            description="Read a book",
            category="Education",
            periodicity="Daily",
            start_date=datetime.now(),
            goal="Read 30 minutes",
            user_id=1
        )
        self.root = tk.Tk()
        self.root.withdraw()
        self.analytics = AnalyticsInterface(root=self.root, current_user_id=self.habit.user_id)

    def tearDown(self):
        self.root.destroy()

    def test_create_habit_invalid_name(self):
        with self.assertRaises(ValueError):
            Habit(
                habit_id=None,
                user_id=1,
                name="",
                description="A test with invalid name",
                category="Test",
                periodicity="Daily",
                start_date="2024-01-01",
                current_streak=0,
                goal="10 days",
                next_deadline=None
            )

    def test_create_habit_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            Habit(
                habit_id=None,
                user_id=1,
                name="Invalid Periodicity Habit",
                description="A habit to test invalid periodicity",
                category="Test",
                periodicity="Invalid",
                start_date="2024-01-01",
                current_streak=0,
                goal="10 days",
                next_deadline=None
            )

    def test_create_habit_success(self):
        habit = Habit(
            habit_id=None,
            user_id=1,
            name="Test Successful Habit",
            description="A habit for successful creation test",
            category="Test",
            periodicity="Daily",
            start_date="2024-01-01",
            current_streak=0,
            goal="10 days",
            next_deadline=None
        )
        habit.save_to_db()
        self.assertIsNotNone(habit.habit_id)

    def test_edit_habit(self):
        new_name = "Read More"
        new_description = "Read a book for an hour"
        new_category = "Self-Improvement"
        new_periodicity = "Weekly"
        new_goal = "Read 1 hour"

        self.habit.name = new_name
        self.habit.description = new_description
        self.habit.category = new_category
        self.habit.periodicity = new_periodicity
        self.habit.goal = new_goal

        self.assertEqual(self.habit.name, new_name)
        self.assertEqual(self.habit.description, new_description)
        self.assertEqual(self.habit.category, new_category)
        self.assertEqual(self.habit.periodicity, new_periodicity)
        self.assertEqual(self.habit.goal, new_goal)

    def test_edit_habit_start_date(self):
        new_start_date = datetime.now() + timedelta(days=1)
        self.habit.start_date = new_start_date
        self.assertEqual(self.habit.start_date, new_start_date)

    def test_edit_habit_next_deadline(self):
        new_next_deadline = datetime.now() + timedelta(days=7)
        self.habit.next_deadline = new_next_deadline
        self.assertEqual(self.habit.next_deadline, new_next_deadline)

    def test_get_habit_overview(self):
        overview = self.analytics.show_habit_overview()
        total_habits, completion_rate, avg_streaks, health_score, recent_activity, most_consistent, least_consistent = overview
        self.assertIsInstance(total_habits, int)
        self.assertIsInstance(completion_rate, float)
        self.assertIsInstance(avg_streaks, float)


    def test_get_streaks_and_consistency(self):
        streaks = self.analytics.show_streaks_consistency()
        self.assertIsNotNone(streaks)

    def test_categorization_analysis(self):
        categories = self.analytics.show_categorization_analysis()
        category_names = [cat[0] for cat in categories]
        self.assertIn('Education', category_names)

    def test_time_analysis(self):
        day_data, month_data, year_data = self.analytics.show_time_analysis()
        self.assertTrue(isinstance(day_data, list))
        self.assertTrue(isinstance(month_data, list))
        self.assertTrue(isinstance(year_data, list))
        self.assertTrue(all(isinstance(x, tuple) for x in day_data))

if __name__ == '__main__':
    unittest.main()
