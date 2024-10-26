import os
import calendar
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from database.db_manager import DBManager
import matplotlib.pyplot as plt  
from datetime import timedelta




class AnalyticsInterface:
    def __init__(self, root, current_user_id):
        self.root = root
        self.current_user_id = current_user_id
        self.db_path = DBManager.get_db_path()  
        print("Database path:", os.path.abspath(self.db_path))  

    def get_db_connection(self):
        print("Connecting to database at:", self.db_path)  
        conn = sqlite3.connect(self.db_path)
        return conn

    def show_habit_overview(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Habit WHERE UserId=?", (self.current_user_id,))
            total_habits = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM HabitRecord
                INNER JOIN Habit ON Habit.HabitId = HabitRecord.HabitId
                WHERE Habit.UserId = ? AND HabitRecord.Success = 1
            """, (self.current_user_id,))
            successful_records = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM HabitRecord
                INNER JOIN Habit ON Habit.HabitId = HabitRecord.HabitId
                WHERE Habit.UserId = ?
            """, (self.current_user_id,))
            total_records = cursor.fetchone()[0]

            completion_rate = (successful_records / total_records * 100) if total_records > 0 else 0

            cursor.execute("SELECT AVG(CurrentStreak) FROM Habit WHERE UserId=?", (self.current_user_id,))
            average_streaks = cursor.fetchone()[0]


            completion_rate_score = completion_rate / 10
            average_streaks_score = min(average_streaks / 10, 10)
            health_score = (completion_rate_score * 0.6) + (average_streaks_score * 0.4)



            cursor.execute("""
                SELECT Habit.Name, HabitRecord.LogDate
                FROM HabitRecord
                INNER JOIN Habit ON Habit.HabitId = HabitRecord.HabitId
                WHERE Habit.UserId = ? AND HabitRecord.Success = 1
                ORDER BY HabitRecord.LogDate DESC
                LIMIT 5
            """, (self.current_user_id,))
            recent_activity = cursor.fetchall()

            cursor.execute("""
                SELECT Habit.Name, ROUND(SUM(CASE WHEN HabitRecord.Success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS SuccessRate
                FROM Habit
                LEFT JOIN HabitRecord ON Habit.HabitId = HabitRecord.HabitId
                WHERE Habit.UserId = ? AND HabitRecord.Success IS NOT NULL
                GROUP BY Habit.HabitId
                HAVING COUNT(*) > 0
                ORDER BY SuccessRate DESC, Habit.Name ASC
                LIMIT 3
            """, (self.current_user_id,))
            most_consistent_habits = cursor.fetchall()

            cursor.execute("""
                SELECT Habit.Name, ROUND(SUM(CASE WHEN HabitRecord.Success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS SuccessRate
                FROM Habit
                LEFT JOIN HabitRecord ON Habit.HabitId = HabitRecord.HabitId
                WHERE Habit.UserId = ? AND HabitRecord.Success IS NOT NULL
                GROUP BY Habit.HabitId
                HAVING COUNT(*) > 0
                ORDER BY SuccessRate ASC, Habit.Name ASC
                LIMIT 3
            """, (self.current_user_id,))
            least_consistent_habits = cursor.fetchall()

            conn.close()

            return total_habits, completion_rate, average_streaks, health_score, recent_activity, most_consistent_habits, least_consistent_habits
        except sqlite3.Error as e:
            print("An error occurred:", e)
            return None, None, None, None, None, None, None



    def show_habit_performance(self, current_user_id):

        habit_performance_window = ctk.CTkToplevel(self.root)
        habit_performance_window.title("Habit Performance")
        habit_performance_window.geometry("400x500")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Habit WHERE UserId = ?", (self.current_user_id,))
        habits = [row[0] for row in cursor.fetchall()]
        conn.close()

        habit_var = tk.StringVar(habit_performance_window)
        habit_var.set(habits[0])  
        habit_dropdown = ttk.Combobox(habit_performance_window, textvariable=habit_var, values=habits)
        habit_dropdown.pack(pady=10)

        current_year = datetime.now().year
        current_month = datetime.now().month

        year_var = tk.IntVar(habit_performance_window)
        year_var.set(current_year)
        year_dropdown = ttk.Combobox(habit_performance_window, textvariable=year_var, values=list(range(current_year - 5, current_year + 1)))
        year_dropdown.pack(pady=5)

        month_var = tk.IntVar(habit_performance_window)
        month_var.set(current_month)
        month_dropdown = ttk.Combobox(habit_performance_window, textvariable=month_var, values=list(range(1, 13)))
        month_dropdown.pack(pady=5)

        calendar_frame = ctk.CTkFrame(habit_performance_window)
        calendar_frame.pack(pady=10)

        def update_calendar(*args):
            selected_habit = habit_var.get()
            selected_year = year_var.get()
            selected_month = month_var.get()

            print(f"Selected habit: {selected_habit}")  

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DATE(LogDate) AS Date, Success
                FROM HabitRecord
                INNER JOIN Habit ON HabitRecord.HabitId = Habit.HabitId
                WHERE Habit.Name = ? AND Habit.UserId = ?
                ORDER BY Date
            """, (selected_habit, self.current_user_id))
            habit_records = cursor.fetchall()
            conn.close()

            print(f"Habit records: {habit_records}")  

            num_days = calendar.monthrange(selected_year, selected_month)[1]

            calendar_matrix = np.zeros((6, 7), dtype=int)

            for record_date_str, success in habit_records:
                record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
                if record_date.year == selected_year and record_date.month == selected_month:
                    row = (record_date.day - 1) // 7
                    col = (record_date.weekday() + 1) % 7
                    calendar_matrix[row, col] = 1 if success else -1

            print(f"Calendar matrix:\n{calendar_matrix}")  

            for widget in calendar_frame.winfo_children():
                widget.destroy()

            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for col, weekday in enumerate(weekdays):
                label = ctk.CTkLabel(calendar_frame, text=weekday)
                label.grid(row=0, column=col, padx=5, pady=5)

            for row in range(6):
                for col in range(7):
                    day = row * 7 + col + 1
                    if day <= num_days:
                        if calendar_matrix[row, col] == 1:
                            color = "green"
                        elif calendar_matrix[row, col] == -1:
                            color = "red"
                        else:
                            color = "gray"
                        label = ctk.CTkLabel(calendar_frame, text=str(day), fg_color=color)
                        label.grid(row=row+1, column=col, padx=5, pady=5)

        habit_var.trace('w', update_calendar)
        year_var.trace('w', update_calendar)
        month_var.trace('w', update_calendar)

        update_calendar()



    def show_streaks_consistency(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Habit.Name, Habit.CurrentStreak, Habit.Periodicity
            FROM Habit
            WHERE Habit.UserId = ?
            ORDER BY Habit.CurrentStreak DESC
        """, (self.current_user_id,))

        habits_data = cursor.fetchall()

        conn.close()

        # Update the streak calculation based on periodicity
        updated_habits_data = []
        for habit_name, current_streak, periodicity in habits_data:
            if periodicity == 'Daily':
                updated_streak = current_streak
            elif periodicity == 'Weekly':
                updated_streak = current_streak * 7
            elif periodicity == 'Monthly':
                updated_streak = current_streak * 30
            else:
                updated_streak = current_streak

            updated_habits_data.append((habit_name, updated_streak))

        return updated_habits_data




    def show_categorization_analysis(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT Category, COUNT(*) AS Count
                FROM Habit
                WHERE UserId = ?
                GROUP BY Category
            """, (self.current_user_id,))
            category_data = cursor.fetchall()

            conn.close()

            return category_data
        except sqlite3.Error as e:
            print("An error occurred:", e)
            return []  


    def show_time_analysis(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT strftime('%w', LogDate) AS DayOfWeek, COUNT(*) AS Count
                FROM HabitRecord
                INNER JOIN Habit ON HabitRecord.HabitId = Habit.HabitId
                WHERE Habit.UserId = ?
                GROUP BY DayOfWeek
            """, (self.current_user_id,))
            day_data = cursor.fetchall()

            cursor.execute("""
                SELECT strftime('%m', LogDate) AS Month, COUNT(*) AS Count
                FROM HabitRecord
                INNER JOIN Habit ON HabitRecord.HabitId = Habit.HabitId
                WHERE Habit.UserId = ?
                GROUP BY Month
            """, (self.current_user_id,))
            month_data = cursor.fetchall()

            cursor.execute("""
                SELECT strftime('%Y', LogDate) AS Year, COUNT(*) AS Count
                FROM HabitRecord
                INNER JOIN Habit ON HabitRecord.HabitId = Habit.HabitId
                WHERE Habit.UserId = ?
                GROUP BY Year
            """, (self.current_user_id,))
            year_data = cursor.fetchall()

            conn.close()

            return day_data, month_data, year_data
        except sqlite3.Error as e:
            print("An error occurred:", e)
            return [], [], []  






