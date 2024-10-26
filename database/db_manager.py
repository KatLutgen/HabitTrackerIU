import sqlite3
import os
import json
from datetime import datetime
from tkinter import messagebox

from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord


class DBManager:

    @staticmethod
    def get_db_path():
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_dir, 'database', 'DataBase.db')
        return db_path

    @staticmethod
    def initialize_database():
        db_path = DBManager.get_db_path()
        print("Initializing database at:", db_path)

        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            print("Creating User table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Username TEXT NOT NULL,
                    Password TEXT NOT NULL,
                    Email TEXT,
                    AccountCreated TEXT,
                    LastLogin TEXT,
                    Status TEXT,
                    ProfilePicture TEXT
                )
            ''')
            print("User table created.")

            print("Creating Habit table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Habit (
                    HabitId INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserId INTEGER,
                    Name TEXT,
                    Description TEXT,
                    Category TEXT,
                    Periodicity TEXT,
                    StartDate TEXT,
                    Goal TEXT,
                    CurrentStreak INTEGER,
                    NextDeadline TEXT,
                    FOREIGN KEY (UserId) REFERENCES User(UserId)
                )
            ''')
            print("Habit table created.")

            print("Creating HabitRecord table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS HabitRecord (
                    RecordId INTEGER PRIMARY KEY AUTOINCREMENT,
                    HabitId INTEGER,
                    LogDate TEXT,
                    Note TEXT,
                    Success INTEGER,
                    Rating INTEGER,
                    FOREIGN KEY (HabitId) REFERENCES Habit(HabitId)
                )
            ''')
            print("HabitRecord table created.")

            connection.commit()
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print("Error initializing the database:", e)
        finally:
            if connection:
                connection.close()



    @staticmethod
    def create_connection():
        db_path = DBManager.get_db_path()
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(e)
        return conn




    @staticmethod
    def get_user_by_username(username):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            user = User(
                user_data[1],  
                user_data[2], 
                user_data[3], 
                user_data[4] if len(user_data) > 4 else "", 
                user_data[8] if len(user_data) > 8 else ""   
            )
            user.user_id = user_data[0]
            user.account_created = user_data[5] if len(user_data) > 5 else None
            user.last_login = user_data[6] if len(user_data) > 6 else None
            user.status = user_data[7] if len(user_data) > 7 else None
            return user
        else:
            return None

    @staticmethod
    def save_user_to_db(user):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO User (Name, Username, Password, Email, AccountCreated, LastLogin, Status, ProfilePicture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.name, user.username, user.password, user.email, user.account_created, user.last_login, user.status, user.profile_picture))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_from_db(user_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE UserId=?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User(
                user_data[1], 
                user_data[2],  
                user_data[3],  
                user_data[4],  
                user_data[8]   
            )
            user.user_id = user_data[0]
            user.account_created = user_data[5]
            user.last_login = user_data[6]
            user.status = user_data[7]
            return user
        else:
            return None

    @staticmethod
    def save_habit_to_db(habit):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO Habit (UserID, Name, Description, Category, Periodicity, StartDate, Goal, CurrentStreak, NextDeadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (habit.user_id, habit.name, habit.description, habit.category, habit.periodicity, habit.start_date, habit.goal, habit.current_streak, habit.next_deadline))

        habit_id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()

        return habit_id






    @staticmethod
    def get_habit_from_db(habit_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habit WHERE HabitId=?", (habit_id,))
        habit_data = cursor.fetchone()
        conn.close()
        if habit_data:
            habit = Habit(
                habit_data[2], 
                habit_data[3],  
                habit_data[4],  
                habit_data[5],  
                datetime.fromisoformat(habit_data[6]), 
                habit_data[8],  
                habit_data[1], 
                habit_data[7],  
                datetime.fromisoformat(habit_data[9]),  
                habit_data[0]  
            )
            habit.records = HabitRecord.load_for_habit(habit_id)  
            return habit
        else:
            return None

    @staticmethod
    def get_habits_by_user_id(user_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habit WHERE UserId=?", (user_id,))
        habits_data = cursor.fetchall()
        habits = []
        for habit_data in habits_data:
            reminders = None
            if habit_data[9]:
                try:
                    reminders = json.loads(habit_data[9])
                except json.JSONDecodeError:
                    print(f"Invalid JSON string for reminders: {habit_data[9]}")
            next_deadline = None
            if len(habit_data) > 10 and habit_data[10]:
                next_deadline = datetime.fromisoformat(habit_data[10])
            habit = Habit(
                habit_data[2],  
                habit_data[3],  
                habit_data[4],  
                habit_data[5],  
                datetime.fromisoformat(habit_data[6]),  
                habit_data[8], 
                user_id,  
                current_streak=habit_data[7],  
                next_deadline=next_deadline,  
                habit_id=habit_data[0]  
            )

            cursor.execute("SELECT * FROM HabitRecord WHERE HabitId=?", (habit.habit_id,))
            records_data = cursor.fetchall()
            records = []
            for record_data in records_data:
                record = HabitRecord(
                    record_data[1],  
                    record_data[3],  
                    bool(record_data[4]),  
                    record_data[5]  
                )
                record.log_date = datetime.fromisoformat(record_data[2])  
                records.append(record)

            habit.records = records
            habits.append(habit)

        conn.close()
        return habits





    @staticmethod
    def save_user_to_db(user):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        if user.user_id is None:
            cursor.execute('''
                INSERT INTO User (Name, Username, Password, Email, AccountCreated, LastLogin, Status, ProfilePicture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user.name, user.username, user.password, user.email, user.account_created, user.last_login, user.status, user.profile_picture))
        else:
            cursor.execute('''
                UPDATE User
                SET Name = ?, Username = ?, Password = ?, Email = ?, LastLogin = ?, Status = ?, ProfilePicture = ?
                WHERE UserId = ?
            ''', (user.name, user.username, user.password, user.email, user.last_login, user.status, user.profile_picture, user.user_id))

        conn.commit()
        conn.close()



    @staticmethod
    def get_user_from_db(user_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE UserId=?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User(
                user_data[1],  
                user_data[2],  
                user_data[3],  
                user_data[4],  
                user_data[8]   
            )
            user.user_id = user_data[0]
            user.account_created = user_data[5]
            user.last_login = user_data[6]
            user.status = user_data[7]
            return user
        else:
            return None

    @staticmethod
    def get_user_by_username(username):
        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User(
                user_data[1], 
                user_data[2], 
                user_data[3],  
                user_data[4] if len(user_data) > 4 else "",  
                user_data[8] if len(user_data) > 8 else ""   
            )
            user.user_id = user_data[0]
            user.account_created = user_data[5] if len(user_data) > 5 else None
            user.last_login = user_data[6] if len(user_data) > 6 else None
            user.status = user_data[7] if len(user_data) > 7 else None
            return user
        else:
            return None

    @staticmethod
    def add_user(name, username, password):
        new_user = User(name=name, username=username, password=password)

        conn = DBManager.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO User (Name, Username, Password)
            VALUES (?, ?, ?)
        ''', (new_user.name, new_user.username, new_user.password))
        conn.commit()
        conn.close()

        print(f"Added user to database: {new_user}")  
        return new_user

    @staticmethod
    def save_habit_record_to_db(habit_record):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO HabitRecord (HabitId, LogDate, Note, Success, Rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (habit_record.habit_id, habit_record.log_date, habit_record.note, habit_record.success, habit_record.rating))

        conn.commit()
        conn.close()

    @staticmethod
    def load_habit_records_for_habit(habit_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM HabitRecord WHERE HabitId=?", (habit_id,))
        records_data = cursor.fetchall()
        conn.close()

        records = []
        for record_data in records_data:
            record = HabitRecord(
                record_data[1], 
                record_data[3],  
                bool(record_data[4]),  
                record_data[5]  
            )
            records.append(record)

        return records

    @staticmethod
    def log_habit_in_db(habit_id, log_date, note="", success=True, rating=None):
        new_record = HabitRecord(habit_id, note, success, rating)
        DBManager.save_habit_record_to_db(new_record)

    @staticmethod
    def authenticate_user(username, password):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user:
            user_id = user[0]
            stored_password = user[3]
            if password == stored_password:
                return True, user_id
            else:
                return False, None
        else:
            return False, None

    @staticmethod
    def get_user_id(username):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id FROM User WHERE Username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving user ID from the database: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_habit_from_db(user_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Habit WHERE UserId = ?", (user_id,))
        habits = cursor.fetchall()

        habit_list = []
        for habit in habits:
            habit_dict = {
                'id': habit[0],
                'user_id': habit[1],
                'name': habit[2],
                'description': habit[3],
                'category': habit[4],
                'periodicity': habit[5],
                'start_date': habit[6],
                'goal': habit[7],
                'current_streak': habit[8],
                'next_deadline': habit[9]
            }
            habit_list.append(habit_dict)

        conn.close()
        return habit_list

    @staticmethod
    def update_habit_in_db(habit):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Habit
            SET Name = ?, Description = ?, Category = ?, Periodicity = ?, Goal = ?
            WHERE HabitId = ?
        """, (habit.name, habit.description, habit.category, habit.periodicity, habit.goal, habit.habit_id))

        conn.commit()
        conn.close()


    def load_test_data(current_user_id):
        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM HabitRecord WHERE HabitId IN (SELECT HabitId FROM Habit WHERE UserId = ?)", (current_user_id,))
        cursor.execute("DELETE FROM Habit WHERE UserId = ?", (current_user_id,))
        conn.commit()

        habits = [
            (current_user_id, 'Morning Run', 'Go for a 30-minute run every morning', 'Fitness', 'Daily', '2022-01-01', '30 minutes', 120, '2023-05-31'),
            (current_user_id, 'Learn Spanish', 'Practice Spanish using a language learning app', 'Education', 'Daily', '2022-03-15', '20 minutes', 75, '2023-06-15'),
            (current_user_id, 'Gratitude Journal', 'Write down three things to be grateful for each day', 'Mindfulness', 'Daily', '2022-02-01', '10 minutes', 100, '2023-06-01'),
            (current_user_id, 'Reading Challenge', 'Read one chapter of a book every day', 'Personal Growth', 'Daily', '2022-04-01', '1 chapter', 60, '2023-05-31'),
            (current_user_id, 'Yoga Practice', 'Attend a yoga class or practice at home', 'Health', 'Weekly', '2022-01-15', '1 hour', 20, '2023-06-30'),
            (current_user_id, 'Meditation', 'Meditate for 10 minutes every morning', 'Mindfulness & Meditation', 'Daily', '2022-01-01', '10 minutes', 90, '2023-06-30'),
            (current_user_id, 'Painting', 'Paint for 30 minutes every weekend', 'Creativity & Art', 'Weekly', '2022-02-01', '30 minutes', 15, '2023-07-01'),
            (current_user_id, 'Saving Money', 'Save 10% of monthly income', 'Financial Management', 'Monthly', '2022-01-01', '10% of income', 6, '2023-06-30'),
            (current_user_id, 'Volunteering', 'Volunteer at a local charity once a month', 'Social & Relationships', 'Monthly', '2022-01-01', '2 hours', 5, '2023-06-30'),
            (current_user_id, 'Recycling', 'Recycle all recyclable waste', 'Environmental Consciousness', 'Daily', '2022-01-01', 'All recyclable waste', 150, '2023-06-30'),
            (current_user_id, 'Healthy Eating', 'Eat at least one serving of vegetables with every meal', 'Health', 'Daily', '2022-05-01', '3 servings', 200, '2023-07-01'),
            (current_user_id, 'Water Intake', 'Drink 8 glasses of water a day', 'Health', 'Daily', '2022-01-15', '8 glasses', 180, '2023-06-30'),
            (current_user_id, 'Declutter', 'Declutter one area of the home each month', 'Home Improvement', 'Monthly', '2022-03-01', '1 area', 12, '2023-06-01'),
            (current_user_id, 'Cooking New Recipes', 'Try cooking a new recipe every week', 'Cooking & Food', 'Weekly', '2022-02-01', '1 recipe', 25, '2023-06-01'),
            (current_user_id, 'Podcast Listening', 'Listen to an educational podcast episode each week', 'Education', 'Weekly', '2022-04-01', '1 episode', 20, '2023-06-15'),
            (current_user_id, 'Strength Training', 'Do a strength training workout twice a week', 'Fitness', 'Weekly', '2022-01-10', '2 sessions', 50, '2023-05-31'),
            (current_user_id, 'Family Time', 'Spend quality time with family every Sunday', 'Social & Relationships', 'Weekly', '2022-01-01', '2 hours', 52, '2023-06-30'),
            (current_user_id, 'Learning Coding', 'Complete one coding lesson every day', 'Education', 'Daily', '2022-01-20', '1 lesson', 90, '2023-05-31'),
            (current_user_id, 'Weekly Reflection', 'Reflect on the week and set goals every Sunday', 'Personal Growth', 'Weekly', '2022-02-01', '30 minutes', 25, '2023-06-15'),
            (current_user_id, 'Digital Detox', 'Take a break from screens for an hour before bed', 'Mindfulness & Meditation', 'Daily', '2022-03-01', '1 hour', 100, '2023-07-01'),
            (current_user_id, 'Gardening', 'Spend an hour gardening every weekend', 'Outdoor Activities', 'Weekly', '2022-04-01', '1 hour', 20, '2023-07-01'),
            (current_user_id, 'Budget Review', 'Review and adjust budget monthly', 'Financial Management', 'Monthly', '2022-01-01', '1 hour', 12, '2023-06-30'),
            (current_user_id, 'Language Exchange', 'Have a language exchange conversation once a week', 'Social & Relationships', 'Weekly', '2022-02-15', '1 hour', 20, '2023-06-15'),
            (current_user_id, 'Photography', 'Take a photo a day to capture a moment', 'Creativity & Art', 'Daily', '2022-03-01', '1 photo', 120, '2023-06-30'),
            (current_user_id, 'Networking', 'Attend a networking event or meeting monthly', 'Career Development', 'Monthly', '2022-01-10', '2 hours', 6, '2023-05-31')
        ]



        conn = DBManager.create_connection()
        cursor = conn.cursor()

        cursor.executemany('''
            INSERT INTO Habit (UserId, Name, Description, Category, Periodicity, StartDate, Goal, CurrentStreak, NextDeadline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', habits)

        conn.commit()

        cursor.execute("SELECT HabitId, Name FROM Habit WHERE UserId = ?", (current_user_id,))
        habit_ids = {name: habit_id for habit_id, name in cursor.fetchall()}

        habit_records = [
        (habit_ids['Morning Run'], '2024-01-05', 'Completed 30-minute run', 1, 5),
        (habit_ids['Morning Run'], '2024-01-06', 'Ran for 25 minutes', 1, 4),
        (habit_ids['Morning Run'], '2024-01-07', 'Skipped run due to rain', 0, 2),
        (habit_ids['Morning Run'], '2024-01-08', 'Ran for 35 minutes', 1, 5),
        (habit_ids['Morning Run'], '2024-01-09', 'Completed 30-minute run', 1, 5),
        (habit_ids['Morning Run'], '2024-01-10', 'Skipped run', 0, 2),
        (habit_ids['Morning Run'], '2024-01-11', 'Ran for 40 minutes', 1, 5),
        (habit_ids['Morning Run'], '2024-01-12', 'Completed 30-minute run', 1, 5),
        (habit_ids['Morning Run'], '2024-01-13', 'Skipped run due to injury', 0, 1),
        (habit_ids['Morning Run'], '2024-01-14', 'Ran for 30 minutes', 1, 5),
        (habit_ids['Learn Spanish'], '2024-02-10', 'Completed Spanish lesson', 1, 4),
        (habit_ids['Learn Spanish'], '2024-02-11', 'Skipped Spanish practice', 0, 2),
        (habit_ids['Learn Spanish'], '2024-02-12', 'Practiced Spanish for 25 minutes', 1, 3),
        (habit_ids['Learn Spanish'], '2024-02-13', 'Completed Spanish lesson', 1, 5),
        (habit_ids['Learn Spanish'], '2024-02-14', 'Practiced Spanish for 20 minutes', 1, 4),
        (habit_ids['Learn Spanish'], '2024-02-15', 'Skipped Spanish practice', 0, 2),
        (habit_ids['Learn Spanish'], '2024-02-16', 'Completed Spanish lesson', 1, 5),
        (habit_ids['Learn Spanish'], '2024-02-17', 'Practiced Spanish for 30 minutes', 1, 4),
        (habit_ids['Gratitude Journal'], '2024-01-28', 'Wrote three gratitude entries', 1, 5),
        (habit_ids['Gratitude Journal'], '2024-01-29', 'Skipped gratitude journal', 0, 2),
        (habit_ids['Gratitude Journal'], '2024-01-30', 'Wrote two gratitude entries', 1, 4),
        (habit_ids['Gratitude Journal'], '2024-01-31', 'Wrote three gratitude entries', 1, 5),
        (habit_ids['Gratitude Journal'], '2024-02-01', 'Wrote three gratitude entries', 1, 5),
        (habit_ids['Gratitude Journal'], '2024-02-02', 'Wrote one gratitude entry', 1, 3),
        (habit_ids['Gratitude Journal'], '2024-02-03', 'Skipped gratitude journal', 0, 2),
        (habit_ids['Gratitude Journal'], '2024-02-04', 'Wrote three gratitude entries', 1, 5),
        (habit_ids['Reading Challenge'], '2024-03-27', 'Read one chapter', 1, 4),
        (habit_ids['Reading Challenge'], '2024-03-28', 'Skipped reading', 0, 2),
        (habit_ids['Reading Challenge'], '2024-03-29', 'Read two chapters', 1, 5),
        (habit_ids['Reading Challenge'], '2024-03-30', 'Read one chapter', 1, 4),
        (habit_ids['Reading Challenge'], '2024-03-31', 'Read one chapter', 1, 4),
        (habit_ids['Reading Challenge'], '2024-04-01', 'Skipped reading', 0, 2),
        (habit_ids['Reading Challenge'], '2024-04-02', 'Read one chapter', 1, 4),
        (habit_ids['Reading Challenge'], '2024-04-03', 'Read three chapters', 1, 5),
        (habit_ids['Yoga Practice'], '2024-04-03', 'Attended yoga class', 1, 5),
        (habit_ids['Yoga Practice'], '2024-04-10', 'Practiced yoga at home', 1, 4),
        (habit_ids['Yoga Practice'], '2024-04-17', 'Skipped yoga practice', 0, 2),
        (habit_ids['Yoga Practice'], '2024-04-24', 'Attended yoga class', 1, 5),
        (habit_ids['Yoga Practice'], '2024-05-01', 'Practiced yoga at home', 1, 4),
        (habit_ids['Yoga Practice'], '2024-05-08', 'Attended yoga class', 1, 5),
        (habit_ids['Meditation'], '2024-05-18', 'Completed 10-minute meditation', 1, 5),
        (habit_ids['Meditation'], '2024-05-19', 'Meditated for 12 minutes', 1, 4),
        (habit_ids['Meditation'], '2024-05-20', 'Skipped meditation', 0, 2),
        (habit_ids['Meditation'], '2024-05-21', 'Completed 10-minute meditation', 1, 5),
        (habit_ids['Meditation'], '2024-05-22', 'Meditated for 15 minutes', 1, 5),
        (habit_ids['Meditation'], '2024-05-23', 'Completed 10-minute meditation', 1, 5),
        (habit_ids['Painting'], '2024-04-24', 'Painted for 45 minutes', 1, 5),
        (habit_ids['Painting'], '2024-05-01', 'Painted for 30 minutes', 1, 4),
        (habit_ids['Painting'], '2024-05-08', 'Skipped painting session', 0, 2),
        (habit_ids['Painting'], '2024-05-15', 'Painted for 1 hour', 1, 5),
        (habit_ids['Painting'], '2024-05-22', 'Painted for 30 minutes', 1, 4),
        (habit_ids['Saving Money'], '2024-01-01', 'Saved 10% of income', 1, 5),
        (habit_ids['Saving Money'], '2024-02-01', 'Saved 10% of income', 1, 5),
        (habit_ids['Saving Money'], '2024-03-01', 'Saved 10% of income', 1, 5),
        (habit_ids['Saving Money'], '2024-04-01', 'Saved 10% of income', 1, 5),
        (habit_ids['Saving Money'], '2024-05-01', 'Saved 10% of income', 1, 5),
        (habit_ids['Volunteering'], '2024-01-15', 'Volunteered at local shelter', 1, 4),
        (habit_ids['Volunteering'], '2024-02-15', 'Volunteered at food bank', 1, 5),
        (habit_ids['Volunteering'], '2024-03-15', 'Missed volunteer session', 0, 2),
        (habit_ids['Volunteering'], '2024-04-15', 'Volunteered at animal shelter', 1, 5),
        (habit_ids['Volunteering'], '2024-05-15', 'Volunteered at local park cleanup', 1, 4),
        (habit_ids['Recycling'], '2024-04-28', 'Recycled all recyclable waste', 1, 5),
        (habit_ids['Recycling'], '2024-04-29', 'Recycled most recyclable waste', 1, 4),
        (habit_ids['Recycling'], '2024-04-30', 'Recycled all recyclable waste', 1, 5),
        (habit_ids['Recycling'], '2024-05-01', 'Missed recycling', 0, 2),
        (habit_ids['Recycling'], '2024-05-02', 'Recycled all recyclable waste', 1, 5),
        (habit_ids['Healthy Eating'], '2024-05-01', 'Ate vegetables with every meal', 1, 5),
        (habit_ids['Healthy Eating'], '2024-05-02', 'Missed vegetable intake for lunch', 0, 3),
        (habit_ids['Healthy Eating'], '2024-05-03', 'Ate vegetables with dinner', 1, 4),
        (habit_ids['Healthy Eating'], '2024-05-04', 'Ate vegetables with every meal', 1, 5),
        (habit_ids['Healthy Eating'], '2024-05-05', 'Missed vegetables at breakfast', 0, 3),
        (habit_ids['Water Intake'], '2024-01-10', 'Drank 8 glasses of water', 1, 5),
        (habit_ids['Water Intake'], '2024-01-11', 'Drank 6 glasses of water', 0, 3),
        (habit_ids['Water Intake'], '2024-01-12', 'Drank 7 glasses of water', 0, 4),
        (habit_ids['Water Intake'], '2024-01-13', 'Drank 8 glasses of water', 1, 5),
        (habit_ids['Water Intake'], '2024-01-14', 'Drank 9 glasses of water', 1, 5),
        (habit_ids['Water Intake'], '2024-01-15', 'Drank 8 glasses of water', 1, 5),
        (habit_ids['Declutter'], '2024-02-01', 'Decluttered kitchen', 1, 5),
        (habit_ids['Declutter'], '2024-03-01', 'Decluttered bedroom', 1, 5),
        (habit_ids['Declutter'], '2024-04-01', 'Decluttered garage', 1, 5),
        (habit_ids['Declutter'], '2024-05-01', 'Decluttered living room', 1, 5),
        (habit_ids['Cooking New Recipes'], '2024-03-15', 'Tried new pasta recipe', 1, 5),
        (habit_ids['Cooking New Recipes'], '2024-03-22', 'Missed cooking session', 0, 2),
        (habit_ids['Cooking New Recipes'], '2024-03-29', 'Cooked new soup recipe', 1, 4),
        (habit_ids['Cooking New Recipes'], '2024-04-05', 'Cooked new dessert recipe', 1, 5),
        (habit_ids['Cooking New Recipes'], '2024-04-12', 'Tried new salad recipe', 1, 4),
        (habit_ids['Podcast Listening'], '2024-04-15', 'Listened to educational podcast', 1, 5),
        (habit_ids['Podcast Listening'], '2024-04-22', 'Missed podcast session', 0, 2),
        (habit_ids['Podcast Listening'], '2024-04-29', 'Listened to health podcast', 1, 4),
        (habit_ids['Podcast Listening'], '2024-05-06', 'Listened to technology podcast', 1, 5),
        (habit_ids['Strength Training'], '2024-03-15', 'Completed strength training', 1, 5),
        (habit_ids['Strength Training'], '2024-03-17', 'Skipped strength training', 0, 2),
        (habit_ids['Strength Training'], '2024-03-20', 'Completed strength training', 1, 5),
        (habit_ids['Strength Training'], '2024-03-22', 'Completed strength training', 1, 5),
        (habit_ids['Strength Training'], '2024-03-25', 'Skipped strength training', 0, 2),
        (habit_ids['Family Time'], '2024-01-21', 'Spent quality time with family', 1, 5),
        (habit_ids['Family Time'], '2024-01-28', 'Spent time with family', 1, 5),
        (habit_ids['Family Time'], '2024-02-04', 'Skipped family time', 0, 2),
        (habit_ids['Family Time'], '2024-02-11', 'Spent quality time with family', 1, 5),
        (habit_ids['Family Time'], '2024-02-18', 'Spent time with family', 1, 5),
        (habit_ids['Learning Coding'], '2024-01-15', 'Completed coding lesson', 1, 5),
        (habit_ids['Learning Coding'], '2024-01-16', 'Completed coding lesson', 1, 5),
        (habit_ids['Learning Coding'], '2024-01-17', 'Skipped coding lesson', 0, 2),
        (habit_ids['Learning Coding'], '2024-01-18', 'Completed coding lesson', 1, 5),
        (habit_ids['Learning Coding'], '2024-01-19', 'Completed coding lesson', 1, 5),
        (habit_ids['Weekly Reflection'], '2024-03-01', 'Reflected on week and set goals', 1, 5),
        (habit_ids['Weekly Reflection'], '2024-03-08', 'Reflected on week and set goals', 1, 5),
        (habit_ids['Weekly Reflection'], '2024-03-15', 'Missed weekly reflection', 0, 2),
        (habit_ids['Weekly Reflection'], '2024-03-22', 'Reflected on week and set goals', 1, 5),
        (habit_ids['Weekly Reflection'], '2024-03-29', 'Reflected on week and set goals', 1, 5),
        (habit_ids['Digital Detox'], '2024-01-01', 'Took break from screens before bed', 1, 5),
        (habit_ids['Digital Detox'], '2024-01-02', 'Skipped digital detox', 0, 2),
        (habit_ids['Digital Detox'], '2024-01-03', 'Took break from screens before bed', 1, 5),
        (habit_ids['Digital Detox'], '2024-01-04', 'Took break from screens before bed', 1, 5),
        (habit_ids['Digital Detox'], '2024-01-05', 'Skipped digital detox', 0, 2),
        (habit_ids['Gardening'], '2024-03-01', 'Spent an hour gardening', 1, 5),
        (habit_ids['Gardening'], '2024-03-08', 'Skipped gardening session', 0, 2),
        (habit_ids['Gardening'], '2024-03-15', 'Spent an hour gardening', 1, 5),
        (habit_ids['Gardening'], '2024-03-22', 'Spent an hour gardening', 1, 5),
        (habit_ids['Gardening'], '2024-03-29', 'Skipped gardening session', 0, 2),
        (habit_ids['Budget Review'], '2024-01-01', 'Reviewed and adjusted budget', 1, 5),
        (habit_ids['Budget Review'], '2024-02-01', 'Reviewed and adjusted budget', 1, 5),
        (habit_ids['Budget Review'], '2024-03-01', 'Reviewed and adjusted budget', 1, 5),
        (habit_ids['Budget Review'], '2024-04-01', 'Reviewed and adjusted budget', 1, 5),
        (habit_ids['Budget Review'], '2024-05-01', 'Reviewed and adjusted budget', 1, 5),
        (habit_ids['Language Exchange'], '2024-01-05', 'Had language exchange conversation', 1, 5),
        (habit_ids['Language Exchange'], '2024-01-12', 'Had language exchange conversation', 1, 5),
        (habit_ids['Language Exchange'], '2024-01-19', 'Missed language exchange', 0, 2),
        (habit_ids['Language Exchange'], '2024-01-26', 'Had language exchange conversation', 1, 5),
        (habit_ids['Language Exchange'], '2024-02-02', 'Had language exchange conversation', 1, 5),
        (habit_ids['Photography'], '2024-02-01', 'Took a photo', 1, 5),
        (habit_ids['Photography'], '2024-02-02', 'Took a photo', 1, 5),
        (habit_ids['Photography'], '2024-02-03', 'Skipped taking a photo', 0, 2),
        (habit_ids['Photography'], '2024-02-04', 'Took a photo', 1, 5),
        (habit_ids['Photography'], '2024-02-05', 'Took a photo', 1, 5),
        (habit_ids['Networking'], '2024-01-10', 'Attended networking event', 1, 5),
        (habit_ids['Networking'], '2024-02-10', 'Missed networking event', 0, 2),
        (habit_ids['Networking'], '2024-03-10', 'Attended networking event', 1, 5),
        (habit_ids['Networking'], '2024-04-10', 'Attended networking event', 1, 5),
        (habit_ids['Networking'], '2024-05-10', 'Attended networking event', 1, 5)
    ]



        cursor.executemany('''
            INSERT INTO HabitRecord (HabitId, LogDate, Note, Success, Rating)
            VALUES (?, ?, ?, ?, ?)
        ''', habit_records)

        conn.commit()
        conn.close()



        messagebox.showinfo("Test Data", "Test data loaded successfully!")

