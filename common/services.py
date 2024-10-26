import bcrypt
import logging
from database.db_manager import DBManager
from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord
from tkinter import messagebox


def authenticate_user(username, password):
    user = DBManager.get_user_by_username(username)
    if user and user.password == password:
        return True, user.user_id
    else:
        return False, None


def update_habit_in_db(habit):
    """Update a habit in the database."""
    try:
        return DBManager.update_habit_in_db(habit)
    except Exception as e:
        logging.error(f"Failed to update habit {habit.name}: {e}")
        return False

def register_user(name, username, email, password):
    existing_user = DBManager.get_user_by_username(username)
    if existing_user:
        return False
    else:
        new_user = User(name=name, username=username, email=email, password=password)
        DBManager.save_user_to_db(new_user)
        return True



def get_habit_from_db(user_id):
    """Retrieve habits from the database for a given user ID."""
    try:
        return DBManager.get_habit_from_db(user_id)
    except Exception as e:
        logging.error(f"Failed to retrieve habits for user ID {user_id}: {e}")
        return []

def get_user_id(username):
    """Retrieve the user ID for a given username."""
    try:
        return DBManager.get_user_id(username)
    except Exception as e:
        logging.error(f"Failed to retrieve user ID for username {username}: {e}")
        return None
