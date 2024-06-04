from datetime import datetime

class HabitRecord:
    def __init__(self, habit_id, note, success, rating):
        self.habit_id = habit_id
        self.log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.note = note
        self.success = success
        self.rating = rating

    def set_rating(self, rating: int):
        if 0 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5.")

    def add_notes(self, notes: str):
        self.note = notes
        print(f"Notes for habit {self.habit_id} updated: {self.note}")

    def mark_success(self, success: bool):
        self.success = success
        status = 'successful' if success else 'unsuccessful'
        print(f"Habit {self.habit_id} marked as {status}.")

    def get_details(self) -> str:
        success_text = "Completed" if self.success else "Not completed"
        return (
            f"Habit ID: {self.habit_id}\n"
            f"Completion Date: {self.log_date}\n"
            f"Notes: {self.note}\n"
            f"Success: {success_text}\n"
            f"Rating: {self.rating if self.rating is not None else 'No rating'}"
        )
    
    def save_to_db(self):
        from database.db_manager import DBManager
        DBManager.save_habit_record_to_db(self)

