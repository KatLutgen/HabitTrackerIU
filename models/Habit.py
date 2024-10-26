from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .HabitRecord import HabitRecord
import uuid

class Habit:
    def __init__(self, name, description, category, periodicity, start_date, goal, user_id, current_streak=0, next_deadline=None, habit_id=None):
        self.validate_name(name)
        self.validate_periodicity(periodicity)
        
        self.habit_id = habit_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.category = category
        self.periodicity = periodicity
        self.start_date = start_date
        self.current_streak = current_streak
        self.goal = goal
        self.next_deadline = next_deadline
        self.records = []

        # Save to database and assign habit_id
        if self.habit_id is None:
            self.habit_id = self.save_to_db()

    def validate_name(self, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Habit name cannot be empty")

    def validate_periodicity(self, periodicity):
        valid_periodicities = ["Daily", "Weekly", "Monthly", "Yearly"]
        if periodicity not in valid_periodicities:
            raise ValueError(f"Invalid periodicity. Must be one of {', '.join(valid_periodicities)}")

    def save_to_db(self):
        from database.db_manager import DBManager
        return DBManager.save_habit_to_db(self)

    def complete(self, note: str, rating: int):
        now = datetime.now()
        record_id = str(uuid.uuid4())
        habit_record = HabitRecord(record_id, now, note, True, rating)
        if now <= self.next_deadline:
            self.current_streak += 1
            self.update_deadlines()
            record_id = str(uuid.uuid4())
            self.records.append(HabitRecord(record_id, self.habit_id, now, note, True, rating))
            print(f"Habit '{self.name}' completed successfully. Current streak: {self.current_streak}")
        else:
            self.current_streak = 0
            self.update_deadlines_failed()
            record_id = str(uuid.uuid4())
            self.records.append(HabitRecord(record_id, self.habit_id, now, note, False, rating))
            print(f"Habit '{self.name}' completion failed. Streak reset to 0.")
   
    def delete_from_db(self):
        from database.db_manager import DBManager
        DBManager.delete_habit_from_db(self.habit_id)
        
    def update_deadlines_failed(self):
        self.current_streak = 0
        now = datetime.now()
        self.next_deadline = self.calculate_next_deadline(now, self.periodicity)
        self.start_date = now

    def calculate_next_deadline(self, start_date, periodicity):
        if periodicity == "Daily":
            return start_date + timedelta(days=1)
        elif periodicity == "Weekly":
            return start_date + timedelta(weeks=1)
        elif periodicity == "Monthly":
            return start_date.replace(day=28) + timedelta(days=4)
        else:
            raise ValueError(f"Invalid periodicity: {periodicity}")

    def current_streak_count(self) -> int:
        if not self.records:
            return 0

        sorted_records = sorted(self.records, key=lambda record: record.completion_date, reverse=True)
        streak = 0
        today = datetime.now().date()

        if sorted_records[0].completion_date.date() != today:
            return 0

        for i, record in enumerate(sorted_records):
            if record.completion_date.date() == today - timedelta(days=i):
                if record.success:
                    streak += 1
                else:
                    break
            else:
                break

        return streak

    def get_habit_status(self) -> str:
        now = datetime.now()
        if now <= self.next_deadline:
            return "Active"
        else:
            return "Overdue"

    def get_longest_run_streak(self):
        if not self.records:
            return 0

        completions = sorted(self.records, key=lambda x: x.completion_date)
        longest_streak = 1
        current_streak = 1
        previous_date = completions[0].completion_date

        for completion in completions[1:]:
            if completion.completion_date == previous_date + timedelta(days=1):
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
            previous_date = completion.completion_date

        longest_streak = max(longest_streak, current_streak)
        return longest_streak

    def update_in_db(self):
        from database.db_manager import DBManager
        return DBManager.update_habit_in_db(self)



