import sys
import os
from datetime import datetime, timedelta

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from models.Habit import Habit
from models.HabitRecord import HabitRecord
from tkcalendar import Calendar
from tkcalendar import DateEntry
import sqlite3
from tkinter import simpledialog
from analytics.AnalyticsInterface import AnalyticsInterface
from common.services import authenticate_user, register_user, get_habit_from_db, update_habit_in_db, get_user_id
from database.db_manager import DBManager

import matplotlib.pyplot as plt

import json
from tkinter import filedialog

def start_application():
    DBManager.initialize_database()

def start_screen():
    title_label = ctk.CTkLabel(root, text="Welcome to Habit Tracker", font=ctk.CTkFont(size=30, weight="bold"))
    title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    login_button = ctk.CTkButton(root, text="Login", command=login_clicked)
    login_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    register_button = ctk.CTkButton(root, text="Register", command=register_clicked)
    register_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    exit_button = ctk.CTkButton(root, text="Exit", command=exit_clicked)
    exit_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

def login_clicked():
    login_window = ctk.CTkToplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")

    username_label = ctk.CTkLabel(login_window, text="Username:")
    username_label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
    username_entry = ctk.CTkEntry(login_window)
    username_entry.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

    password_label = ctk.CTkLabel(login_window, text="Password:")
    password_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
    password_entry = ctk.CTkEntry(login_window, show="*")
    password_entry.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def login_submit():
        global current_user_id
        username = username_entry.get()
        password = password_entry.get()
        authenticated, user_id = authenticate_user(username, password)
        if authenticated:
            current_user_id = user_id
            print(f"User ID: {user_id}")
            login_window.destroy()
            show_main_menu(current_user_id)
        else:
            error_label = ctk.CTkLabel(login_window, text="Invalid username or password", text_color="red")
            error_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    login_button = ctk.CTkButton(login_window, text="Login", command=login_submit)
    login_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

def register_clicked():
    register_window = ctk.CTkToplevel(root)
    register_window.title("Register")
    register_window.geometry("400x400")

    name_label = ctk.CTkLabel(register_window, text="Name:")
    name_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
    name_entry = ctk.CTkEntry(register_window)
    name_entry.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

    username_label = ctk.CTkLabel(register_window, text="Username:")
    username_label.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)
    username_entry = ctk.CTkEntry(register_window)
    username_entry.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

    email_label = ctk.CTkLabel(register_window, text="Email:")
    email_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
    email_entry = ctk.CTkEntry(register_window)
    email_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

    password_label = ctk.CTkLabel(register_window, text="Password:")
    password_label.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)
    password_entry = ctk.CTkEntry(register_window, show="*")
    password_entry.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

    confirm_password_label = ctk.CTkLabel(register_window, text="Confirm Password:")
    confirm_password_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
    confirm_password_entry = ctk.CTkEntry(register_window, show="*")
    confirm_password_entry.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

    def register_submit():
        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password == confirm_password:
            if register_user(name, username, email, password):
                messagebox.showinfo("Registration", "User registered successfully!")
                register_window.destroy()
            else:
                messagebox.showerror("Registration", "Username already exists. Please choose a different username.")
        else:
            messagebox.showerror("Registration", "Passwords do not match.")

    register_button = ctk.CTkButton(register_window, text="Register", command=register_submit)
    register_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

def exit_clicked():
    root.destroy()

def show_main_menu(current_user_id):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Main Menu")

    user = DBManager.get_user_from_db(current_user_id)
    if user:
        welcome_text = f"Welcome to Habit Tracker, {user.name}!"
    else:
        welcome_text = "Welcome to Habit Tracker!"

    title_label = ctk.CTkLabel(root, text=welcome_text, font=ctk.CTkFont(size=24, weight="bold"))
    title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    habit_menu_button = ctk.CTkButton(root, text="Habit Menu", command=lambda: habit_menu(current_user_id))
    habit_menu_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

    analysis_button = ctk.CTkButton(root, text="Analysis", command=lambda: open_analysis_menu(current_user_id))
    analysis_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    account_settings_button = ctk.CTkButton(root, text="Account Settings", command=lambda: account_settings(current_user_id))
    account_settings_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    export_button = ctk.CTkButton(root, text="Export Data", command=lambda: export_data(current_user_id))
    export_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)


    def load_test_data_confirmation():
        confirmation = messagebox.askquestion(
            "Confirmation",
            "This action will overwrite any data that is already added to the account and is only for testing purposes.\n"
            "Afterward, you can add your own data, but everything that was added before will be deleted.\n"
            "Are you sure you want to proceed?",
            icon="warning"
        )
        if confirmation == "yes":
            DBManager.load_test_data(current_user_id)
            messagebox.showinfo("Success", "Test data loaded successfully.")
        else:
            messagebox.showinfo("Canceled", "Loading test data canceled.")

    load_data_button = ctk.CTkButton(root, text="Load Test Data", command=load_test_data_confirmation)
    load_data_button.place(relx=0.8, rely=0.9, anchor=ctk.CENTER)

    exit_button = ctk.CTkButton(root, text="Exit Application", command=root.quit)
    exit_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

def account_settings(current_user_id):
    account_settings_window = ctk.CTkToplevel(root)
    account_settings_window.title("Account Settings")
    account_settings_window.geometry("400x400")

    user = DBManager.get_user_from_db(current_user_id)

    name_label = ctk.CTkLabel(account_settings_window, text="Name:")
    name_label.pack()
    name_entry = ctk.CTkEntry(account_settings_window)
    name_entry.insert(0, user.name)
    name_entry.pack()

    username_label = ctk.CTkLabel(account_settings_window, text="Username:")
    username_label.pack()
    username_entry = ctk.CTkEntry(account_settings_window)
    username_entry.insert(0, user.username)
    username_entry.pack()

    email_label = ctk.CTkLabel(account_settings_window, text="Email:")
    email_label.pack()
    email_entry = ctk.CTkEntry(account_settings_window)
    if user.email is not None:
        email_entry.insert(0, user.email)
    email_entry.pack()

    password_label = ctk.CTkLabel(account_settings_window, text="New Password:")
    password_label.pack()
    password_entry = ctk.CTkEntry(account_settings_window, show="*")
    password_entry.pack()

    confirm_password_label = ctk.CTkLabel(account_settings_window, text="Confirm New Password:")
    confirm_password_label.pack()
    confirm_password_entry = ctk.CTkEntry(account_settings_window, show="*")
    confirm_password_entry.pack()

    def update_account():
        new_name = name_entry.get()
        new_username = username_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if new_password == confirm_password:
            user.name = new_name
            user.username = new_username
            user.email = new_email
            if new_password:
                user.password = new_password

            DBManager.save_user_to_db(user)
            messagebox.showinfo("Account Settings", "Account settings updated successfully!")
            account_settings_window.destroy()
        else:
            messagebox.showerror("Account Settings", "New passwords do not match.")



    update_button = ctk.CTkButton(account_settings_window, text="Update", command=update_account)
    update_button.pack(pady=10)

def habit_menu(current_user_id):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Habit Menu")

    title_label = ctk.CTkLabel(root, text="Habit Menu", font=ctk.CTkFont(size=24, weight="bold"))
    title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    view_habits_button = ctk.CTkButton(root, text="View Habits", command=lambda: view_habits(current_user_id))
    view_habits_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

    create_habit_button = ctk.CTkButton(root, text="Create Habit", command=create_habit)
    create_habit_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    edit_habit_button = ctk.CTkButton(root, text="Edit Habit", command=lambda: edit_habit(current_user_id))
    edit_habit_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    log_habit_button = ctk.CTkButton(root, text="Log Habit", command=lambda: log_habit(current_user_id, root))
    log_habit_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

    back_button = ctk.CTkButton(root, text="Back to Main Menu", command=lambda: show_main_menu(current_user_id))
    back_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

def log_habit(user_id, root):
    log_window = tk.Toplevel(root)
    log_window.title("Log Habit")

    habit_listbox = tk.Listbox(log_window)
    habit_listbox.grid(row=0, column=0, padx=10, pady=10)

    conn = DBManager.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Habit WHERE UserId = ?", (user_id,))
    habits = cursor.fetchall()
    conn.close()

    for habit in habits:
        habit_listbox.insert(tk.END, f"{habit[0]}: {habit[2]}")

    def log_selected_habit():
        selection = habit_listbox.curselection()
        if selection:
            selected_habit = habit_listbox.get(selection[0])
            habit_id = int(selected_habit.split(":")[0])

            note = simpledialog.askstring("Input", "Enter any notes (optional):", parent=log_window)
            success = messagebox.askyesno("Question", "Did you complete the habit successfully?")
            rating = simpledialog.askinteger("Input", "Enter a rating (1-5):", parent=log_window, minvalue=1, maxvalue=5)

            habit = get_habit_from_db(habit_id)
            log_date = datetime.now().date()
            new_record = HabitRecord(habit_id, note, success, rating, log_date=log_date)
            new_record.save_to_db()

            update_streak_and_next_deadline(habit, success, log_date)

            messagebox.showinfo("Success", "Habit logged successfully!")
        else:
            messagebox.showwarning("Warning", "No habit selected")

    log_button = tk.Button(log_window, text="Log Habit", command=log_selected_habit)
    log_button.grid(row=1, column=0, padx=10, pady=10)

def update_streak_and_next_deadline(habit, success, log_date):
    if success:
        habit.current_streak += 1
    else:
        habit.current_streak = 0

    if habit.periodicity == "Daily":
        habit.next_deadline = log_date + timedelta(days=1)
    elif habit.periodicity == "Weekly":
        habit.next_deadline = log_date + timedelta(days=7)
    elif habit.periodicity == "Monthly":
        next_month = log_date.replace(day=1) + timedelta(days=32)
        habit.next_deadline = next_month.replace(day=1)
    else:  # Yearly
        next_year = log_date.replace(year=log_date.year + 1)
        habit.next_deadline = next_year

    update_habit_in_db(habit)

def open_analysis_menu(current_user_id):
    analysis_window = ctk.CTkToplevel(root)
    analysis_window.title("Analysis")
    analysis_window.geometry("400x300")

    analytics = AnalyticsInterface(root, current_user_id)

    def show_habit_overview():
        total_habits, completion_rate, average_streaks, health_score, recent_activity, most_consistent_habits, least_consistent_habits = analytics.show_habit_overview()
        if total_habits is not None and completion_rate is not None and average_streaks is not None and health_score is not None and recent_activity is not None and most_consistent_habits is not None and least_consistent_habits is not None:
            habit_overview_window = ctk.CTkToplevel(root)
            habit_overview_window.title("Habit Overview")
            habit_overview_window.geometry("600x800")

            total_habits_label = ctk.CTkLabel(habit_overview_window, text=f"Total Habits: {total_habits}")
            total_habits_label.pack(pady=10)

            completion_rate_label = ctk.CTkLabel(habit_overview_window, text=f"Completion Rate: {completion_rate:.2f}%")
            completion_rate_label.pack(pady=5)

            average_streaks_label = ctk.CTkLabel(habit_overview_window, text=f"Average Streaks: {average_streaks:.2f} days")
            average_streaks_label.pack(pady=5)

            health_score_label = ctk.CTkLabel(habit_overview_window, text=f"Overall Habit Health Score: {health_score:.2f}/10")
            health_score_label.pack(pady=5)

            recent_activity_label = ctk.CTkLabel(habit_overview_window, text="Recent Activity:")
            recent_activity_label.pack(pady=10)

            for habit, log_date in recent_activity:
                activity_label = ctk.CTkLabel(habit_overview_window, text=f"{habit} - {log_date}")
                activity_label.pack(pady=2)

            most_consistent_label = ctk.CTkLabel(habit_overview_window, text="Most Consistent Habits:")
            most_consistent_label.pack(pady=10)

            for habit, completion_rate in most_consistent_habits:
                habit_label = ctk.CTkLabel(habit_overview_window, text=f"{habit} - {completion_rate:.2f}%")
                habit_label.pack(pady=2)

            least_consistent_label = ctk.CTkLabel(habit_overview_window, text="Least Consistent Habits:")
            least_consistent_label.pack(pady=10)

            for habit, completion_rate in least_consistent_habits:
                habit_label = ctk.CTkLabel(habit_overview_window, text=f"{habit} - {completion_rate:.2f}%")
                habit_label.pack(pady=2)

    habit_overview_button = ctk.CTkButton(analysis_window, text="Habit Overview", command=show_habit_overview)
    habit_overview_button.pack(pady=10)

    def show_habit_performance():
        analytics.show_habit_performance(current_user_id)

    habit_performance_button = ctk.CTkButton(analysis_window, text="Habit Performance", command=show_habit_performance)
    habit_performance_button.pack(pady=10)

    streaks_consistency_button = ctk.CTkButton(analysis_window, text="Streaks and Consistency", command=lambda: show_streaks_consistency_window(analytics.show_streaks_consistency()))
    streaks_consistency_button.pack(pady=10)

    categorization_analysis_button = ctk.CTkButton(analysis_window, text="Categorization Analysis", command=lambda: show_categorization_analysis_window(analytics.show_categorization_analysis()))
    categorization_analysis_button.pack(pady=10)

    time_analysis_button = ctk.CTkButton(analysis_window, text="Time Analysis", command=lambda: show_time_analysis_window(*analytics.show_time_analysis()))
    time_analysis_button.pack(pady=10)      

    analysis_window.protocol("WM_DELETE_WINDOW", analysis_window.destroy)
    analysis_window.wait_window()

def show_streaks_consistency_window(habits_data):
    streaks_window = ctk.CTkToplevel(root)
    streaks_window.title("Streaks and Consistency")
    streaks_window.geometry("500x400")

    title_label = ctk.CTkLabel(streaks_window, text="Streaks and Consistency", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    table_frame = ctk.CTkFrame(streaks_window)
    table_frame.pack(padx=20, pady=10)

    headers = ["Habit", "Current Streak"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
        header_label.grid(row=0, column=col, padx=10, pady=5)

    for row, habit_data in enumerate(habits_data, start=1):
        habit_name, current_streak = habit_data
        habit_label = ctk.CTkLabel(table_frame, text=habit_name)
        habit_label.grid(row=row, column=0, padx=10, pady=5)
        current_streak_label = ctk.CTkLabel(table_frame, text=str(current_streak))
        current_streak_label.grid(row=row, column=1, padx=10, pady=5)

    if habits_data:
        motivation_label = ctk.CTkLabel(streaks_window, text="Keep up the great work! Your consistency is paying off.", font=("Arial", 14))
        motivation_label.pack(pady=20)
    else:
        motivation_label = ctk.CTkLabel(streaks_window, text="Start building streaks and stay consistent with your habits.", font=("Arial", 14))
        motivation_label.pack(pady=20)


def show_categorization_analysis_window(category_data):
    categorization_window = ctk.CTkToplevel(root)
    categorization_window.title("Categorization Analysis")
    categorization_window.geometry("500x400")

    title_label = ctk.CTkLabel(categorization_window, text="Categorization Analysis", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    fig, ax = plt.subplots(figsize=(6, 6))

    categories = [data[0] for data in category_data]
    counts = [data[1] for data in category_data]

    ax.pie(counts, labels=categories, autopct='%1.1f%%')
    ax.set_title("Habit Categories")

    canvas = FigureCanvasTkAgg(fig, master=categorization_window)
    canvas.draw()

    canvas.get_tk_widget().pack(pady=10)

    if category_data:
        message_label = ctk.CTkLabel(categorization_window, text="Analyze your habit distribution and identify areas for improvement.", font=("Arial", 14))
        message_label.pack(pady=10)
    else:
        message_label = ctk.CTkLabel(categorization_window, text="No habit data available for categorization analysis.", font=("Arial", 14))
        message_label.pack(pady=10)

def show_time_analysis_window(day_data, month_data, year_data):
    time_analysis_window = ctk.CTkToplevel(root)
    time_analysis_window.title("Time Analysis")
    time_analysis_window.geometry("1000x600")

    title_label = ctk.CTkLabel(time_analysis_window, text="Time Analysis", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = [0] * 7
    for data in day_data:
        day_of_week = int(data[0])
        count = data[1]
        counts[day_of_week] = count
    ax1.bar(days_of_week, counts)
    ax1.set_xlabel("Day of the Week")
    ax1.set_ylabel("Number of Habit Records")
    ax1.set_title("Habit Records by Day of the Week")

    months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    counts = [0] * 12
    for data in month_data:
        month = int(data[0]) - 1
        count = data[1]
        counts[month] = count
    ax2.bar(months, counts)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Number of Habit Records")
    ax2.set_title("Habit Records by Month")

    years = [2022, 2023, 2024]
    counts = [0] * 3
    for data in year_data:
        year = int(data[0])
        count = data[1]
        if year in years:
            index = years.index(year)
            counts[index] = count
    ax3.bar(years, counts)
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Number of Habit Records")
    ax3.set_title("Habit Records by Year")

    plt.subplots_adjust(wspace=0.3)

    canvas = FigureCanvasTkAgg(fig, master=time_analysis_window)
    canvas.draw()

    canvas.get_tk_widget().pack(pady=10)

    if day_data or month_data or year_data:
        message_label = ctk.CTkLabel(time_analysis_window, text="Analyze your habit patterns and identify productive times.", font=("Arial", 14))
        message_label.pack(pady=10)
    else:
        message_label = ctk.CTkLabel(time_analysis_window, text="No habit data available for time analysis.", font=("Arial", 14))
        message_label.pack(pady=10)

def view_habits(user_id):
    view_habits_window = ctk.CTkToplevel(root)
    view_habits_window.title("View Habits")
    view_habits_window.geometry("600x800")

    title_label = ctk.CTkLabel(view_habits_window, text="View Habits", font=ctk.CTkFont(size=16))
    title_label.pack(pady=20)

    options_frame = ctk.CTkFrame(view_habits_window)
    options_frame.pack(pady=10)

    category_dropdown = ctk.CTkComboBox(options_frame, values=["All", "Health & Wellness", "Fitness & Exercise", "Diet & Nutrition", "Mindfulness & Meditation", "Personal Development", "Professional Growth", "Creativity & Art", "Productivity & Organization", "Social & Relationships", "Leisure & Recreation", "Learning & Education", "Financial Management", "Home & Domestic Life", "Spirituality & Religion", "Environmental Consciousness"])
    category_dropdown.pack(side=ctk.LEFT, padx=5)
    category_dropdown.set("All")

    periodicity_dropdown = ctk.CTkComboBox(options_frame, values=["All", "Daily", "Weekly", "Monthly"])
    periodicity_dropdown.pack(side=ctk.LEFT, padx=5)
    periodicity_dropdown.set("All")

    habit_list_frame = ctk.CTkFrame(view_habits_window)
    habit_list_frame.pack(pady=10)

    scrollbar = ctk.CTkScrollbar(habit_list_frame)
    scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

    habit_listbox = tk.Listbox(habit_list_frame, yscrollcommand=scrollbar.set)
    habit_listbox.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    scrollbar.configure(command=habit_listbox.yview)

    def update_habit_list():
        print("Updating habit list...")
        habit_listbox.delete(0, tk.END)

        selected_category = category_dropdown.get()
        selected_periodicity = periodicity_dropdown.get()
        print(f"Selected Category: {selected_category}, Selected Periodicity: {selected_periodicity}")

        habits = get_habit_from_db(user_id)
        print(f"All Habits Count: {len(habits)}")

        filtered_habits = [
            habit for habit in habits
            if (selected_category == "All" or habit['category'] == selected_category)
            and (selected_periodicity == "All" or habit['periodicity'] == selected_periodicity)
        ]
        print(f"Filtered Habits Count: {len(filtered_habits)}")

        for habit in filtered_habits:
            print(f"Habit: {habit}")
            habit_listbox.insert(tk.END, habit['name'])
        if not filtered_habits:
            habit_listbox.insert(tk.END, "No habits found")

        return filtered_habits

    filter_button = ctk.CTkButton(options_frame, text="Filter", command=update_habit_list)
    filter_button.pack(side=ctk.LEFT, padx=5)

    details_frame = ctk.CTkFrame(view_habits_window)
    details_frame.pack(pady=10)

    name_label = ctk.CTkLabel(details_frame, text="")
    name_label.pack()

    description_label = ctk.CTkLabel(details_frame, text="")
    description_label.pack()

    category_label = ctk.CTkLabel(details_frame, text="")
    category_label.pack()

    periodicity_label = ctk.CTkLabel(details_frame, text="")
    periodicity_label.pack()

    start_date_label = ctk.CTkLabel(details_frame, text="")
    start_date_label.pack()

    goal_label = ctk.CTkLabel(details_frame, text="")
    goal_label.pack()

    current_streak_label = ctk.CTkLabel(details_frame, text="")
    current_streak_label.pack()

    next_deadline_label = ctk.CTkLabel(details_frame, text="")
    next_deadline_label.pack()

    def view_habit_details(event):
        selected_index = habit_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_habit = filtered_habits[index]

            name_label.configure(text=f"Name: {selected_habit['name']}")
            description_label.configure(text=f"Description: {selected_habit['description']}")
            category_label.configure(text=f"Category: {selected_habit['category']}")
            periodicity_label.configure(text=f"Periodicity: {selected_habit['periodicity']}")
            start_date_label.configure(text=f"Start Date: {selected_habit['start_date']}")
            goal_label.configure(text=f"Goal: {selected_habit['goal']}")
            current_streak_label.configure(text=f"Current Streak: {selected_habit['current_streak']}")
            next_deadline_label.configure(text=f"Next Deadline: {selected_habit['next_deadline']}")
        else:
            name_label.configure(text="")
            description_label.configure(text="")
            category_label.configure(text="")
            periodicity_label.configure(text="")
            start_date_label.configure(text="")
            goal_label.configure(text="")
            current_streak_label.configure(text="")
            next_deadline_label.configure(text="")

    habit_listbox.bind("<<ListboxSelect>>", view_habit_details)

    close_button = ctk.CTkButton(view_habits_window, text="Close", command=view_habits_window.destroy)
    close_button.pack(pady=10)

    filtered_habits = update_habit_list()

def create_habit():
    create_habit_window = ctk.CTkToplevel(root)
    create_habit_window.title("Create Habit")
    create_habit_window.geometry("400x750")

    habit_name_entry = ctk.CTkEntry(create_habit_window, placeholder_text="Habit Name")
    habit_name_entry.pack(pady=10)

    habit_description_entry = ctk.CTkEntry(create_habit_window, placeholder_text="Habit Description")
    habit_description_entry.pack(pady=10)

    habit_category_combobox = ctk.CTkComboBox(create_habit_window, values=[
        "Health & Wellness",
        "Fitness & Exercise",
        "Diet & Nutrition",
        "Mindfulness & Meditation",
        "Personal Development",
        "Professional Growth",
        "Creativity & Art",
        "Productivity & Organization",
        "Social & Relationships",
        "Leisure & Recreation",
        "Learning & Education",
        "Financial Management",
        "Home & Domestic Life",
        "Spirituality & Religion",
        "Environmental Consciousness"
    ])
    habit_category_combobox.pack(pady=10)

    habit_periodicity_combobox = ctk.CTkComboBox(create_habit_window, values=["Daily", "Weekly", "Monthly"])
    habit_periodicity_combobox.pack(pady=10)

    habit_start_date_calendar = DateEntry(create_habit_window, date_pattern="yyyy-mm-dd")
    habit_start_date_calendar.pack(pady=10)

    habit_goal_entry = ctk.CTkEntry(create_habit_window, placeholder_text="Habit Goal")
    habit_goal_entry.pack(pady=10)

    submit_button = ctk.CTkButton(create_habit_window, text="Create Habit",
                                  command=lambda: create_habit_clicked(habit_name_entry, habit_description_entry,
                                                                       habit_category_combobox,
                                                                       habit_periodicity_combobox,
                                                                       habit_start_date_calendar, habit_goal_entry,
                                                                       current_user_id, create_habit_window))
    submit_button.pack(pady=10)

def create_habit_clicked(habit_name_entry, habit_description_entry, habit_category_combobox,
                         habit_periodicity_combobox,
                         habit_start_date_calendar, habit_goal_entry, user_id, create_habit_window):
    habit_name = habit_name_entry.get()
    habit_description = habit_description_entry.get()
    habit_category = habit_category_combobox.get()
    habit_periodicity = habit_periodicity_combobox.get()
    habit_start_date = habit_start_date_calendar.get_date()
    habit_goal = habit_goal_entry.get()

    next_deadline = calculate_next_deadline(habit_start_date, habit_periodicity)

    habit = Habit(
        name=habit_name,
        description=habit_description,
        category=habit_category,
        periodicity=habit_periodicity,
        start_date=habit_start_date,
        goal=habit_goal,
        user_id=user_id,
        current_streak=0,
        next_deadline=next_deadline
    )

    habit.save_to_db()

    messagebox.showinfo("Success", "Habit created successfully!")
    create_habit_window.destroy()

def calculate_next_deadline(start_date, periodicity):
    if periodicity == "Daily":
        return start_date + timedelta(days=1)
    elif periodicity == "Weekly":
        return start_date + timedelta(days=7)
    elif periodicity == "Monthly":
        next_month = start_date.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=1)
    else:  # Yearly
        return start_date.replace(year=start_date.year + 1)

def edit_habit(user_id):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Habit")

    habit_listbox = tk.Listbox(edit_window)
    habit_listbox.grid(row=0, column=0, padx=10, pady=10)

    habits = get_habit_from_db(user_id)
    populate_habit_listbox(habit_listbox, habits)

    def load_habit_details(event):
        selection = habit_listbox.curselection()
        if selection:
            selected_habit_data = habit_listbox.get(selection[0])
            habit_id, user_id, name, description, category, periodicity, start_date, goal, current_streak, next_deadline = selected_habit_data

            habit_name_entry.delete(0, tk.END)
            habit_name_entry.insert(tk.END, name)

            habit_description_entry.delete(0, tk.END)
            habit_description_entry.insert(tk.END, description)

            habit_category_combobox.set(category)
            habit_periodicity_combobox.set(periodicity)
        else:
            print("No habit selected")

    habit_listbox.bind("<<ListboxSelect>>", load_habit_details)

    habit_name_label = tk.Label(edit_window, text="Name:")
    habit_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    habit_name_entry = tk.Entry(edit_window)
    habit_name_entry.grid(row=1, column=1, padx=10, pady=5)

    habit_description_label = tk.Label(edit_window, text="Description:")
    habit_description_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    habit_description_entry = tk.Entry(edit_window)
    habit_description_entry.grid(row=2, column=1, padx=10, pady=5)

    habit_category_label = tk.Label(edit_window, text="Category:")
    habit_category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    habit_category_combobox = ttk.Combobox(edit_window, values=[
        "Health & Wellness",
        "Fitness & Exercise",
        "Diet & Nutrition",
        "Mindfulness & Meditation",
        "Personal Development",
        "Professional Growth",
        "Creativity & Art",
        "Productivity & Organization",
        "Social & Relationships",
        "Leisure & Recreation",
        "Learning & Education",
        "Financial Management",
        "Home & Domestic Life",
        "Spirituality & Religion",
        "Environmental Consciousness"
    ])
    habit_category_combobox.grid(row=3, column=1, padx=10, pady=5)

    habit_periodicity_label = tk.Label(edit_window, text="Periodicity:")
    habit_periodicity_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    habit_periodicity_combobox = ttk.Combobox(edit_window, values=[
        "Daily",
        "Weekly",
        "Monthly",
        "Yearly"
    ])
    habit_periodicity_combobox.grid(row=4, column=1, padx=10, pady=5)

    def update_habit():
        selection = habit_listbox.curselection()
        if selection:
            selected_habit_data = habit_listbox.get(selection[0])
            habit_id, user_id, name, description, category, periodicity, start_date, goal, current_streak, next_deadline = selected_habit_data

            updated_habit = Habit(
                habit_id=habit_id,
                user_id=user_id,
                name=habit_name_entry.get(),
                description=habit_description_entry.get(),
                category=habit_category_combobox.get(),
                periodicity=habit_periodicity_combobox.get(),
                start_date=start_date,
                goal=goal,
                current_streak=current_streak,
                next_deadline=next_deadline
            )

            update_habit_in_db(updated_habit)

            habits = get_habit_from_db(user_id)
            populate_habit_listbox(habit_listbox, habits)

            messagebox.showinfo("Success", "Habit updated successfully!")
        else:
            print("No habit selected")

    update_button = tk.Button(edit_window, text="Update", command=update_habit)
    update_button.grid(row=5, column=0, padx=10, pady=10)

def populate_habit_listbox(habit_listbox, habits):
    habit_listbox.delete(0, tk.END)
    for habit in habits:
        habit_data = (
            habit['id'],
            habit['user_id'],
            habit['name'],
            habit['description'],
            habit['category'],
            habit['periodicity'],
            habit['start_date'],
            habit['goal'],
            habit['current_streak'],
            habit['next_deadline']
        )
        habit_listbox.insert(tk.END, habit_data)



def export_data(current_user_id):
    user = DBManager.get_user_from_db(current_user_id)
    habits = DBManager.get_habits_by_user_id(current_user_id)

    exported_data = {
        "user": {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "account_created": user.account_created,
            "last_login": user.last_login,
            "status": user.status,
            "profile_picture": user.profile_picture
        },
        "habits": [],
        "habit_records": []
    }

    for habit in habits:
        habit_data = {
            "name": habit.name,
            "description": habit.description,
            "category": habit.category,
            "periodicity": habit.periodicity,
            "start_date": habit.start_date.isoformat(),
            "goal": habit.goal,
            "current_streak": habit.current_streak,
            "next_deadline": habit.next_deadline.isoformat() if habit.next_deadline else None
        }
        exported_data["habits"].append(habit_data)

        for record in habit.records:
            record_data = {
                "habit_id": record.habit_id,
                "log_date": record.log_date.isoformat(),
                "note": record.note,
                "success": record.success,
                "rating": record.rating
            }
            exported_data["habit_records"].append(record_data)

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

    if file_path:
        with open(file_path, "w") as file:
            json.dump(exported_data, file, indent=4)
        messagebox.showinfo("Export Data", "Data exported successfully!")
    else:
        messagebox.showinfo("Export Data", "Export cancelled.")


root = ctk.CTk()
root.geometry("750x450")
root.title("Habit Tracker")

start_screen()

root.mainloop()
