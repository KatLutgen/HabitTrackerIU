# Habit Tracker

Habit Tracker is a Python application designed to help you develop and maintain good habits. It allows you to create, track, and analyze your habits, providing a comprehensive solution for personal growth and self-improvement.

## How To Get Started

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: Ensure you have Git installed. If not, download it from [git-scm.com](https://git-scm.com/downloads).

### Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KatLutgen/HabitTrackerIU.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd HabitTrackerIU
   ```

3. **Run the setup script**:
   The `setup.sh` script will handle the installation of dependencies and setup of the virtual environment for you.
   ```bash
   ./setup.sh
   ```

   If you encounter any permission issues, you may need to run:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

### Manual Setup (if not using `setup.sh`)

If you prefer to set up the project manually, follow these steps:

1. **Install `Tcl/Tk` libraries**:
   - **macOS**:
     ```bash
     brew install python-tk
     ```
   - **Windows**:
     - `tkinter` is usually included with Python. If not, download and install the latest version of Python from [python.org](https://www.python.org/downloads/).

2. **Create and activate a virtual environment**:
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Run The Application

To start the Habit Tracker application, run the following command:
```bash
python3 main/main.py
```



### Notes

- The project includes a `.gitignore` file to exclude unnecessary files and directories from being committed to the repository.
- The **Load Test Data** feature allows users to populate their account with example data for testing purposes. Use with caution as it will overwrite existing data.

---



## User Interface Overview

### 1. Register Screen

The Register screen allows new users to create an account. Users need to fill in the following fields:
- **Name**: Enter your full name.
- **Username**: Choose a unique username.
- **Email**: Provide a valid email address.
- **Password**: Create a secure password.
- **Confirm Password**: Re-enter the password to confirm.

A "Register" button at the bottom submits the registration form. 


### 2. Main Menu

Upon successful login or registration, users are greeted with a welcome message and several options:
- **Habit Menu**: Access the menu for managing habits.
- **Analysis**: View detailed analysis of your habits.
- **Account Settings**: Update your account information.
- **Export Data**: Export your habit data.
- **Exit Application**: Close the application.
- **Load Test Data**: Load example data for testing purposes.

The **Load Test Data** button is designed to help users quickly populate their account with pre-defined habits and logs for testing purposes. This action will overwrite any existing data in the user's account, and it is intended solely for testing. Users should be cautious as this will delete all their current habits and logs.


### 3. Habit Menu

The Habit Menu provides options to manage habits:
- **View Habits**: Display all habits.
- **Create Habit**: Create a new habit.
- **Edit Habit**: Modify existing habits.
- **Log Habit**: Record progress on habits.
- **Back to Main Menu**: Return to the main menu.


### 4. Analysis Menu

The Analysis Menu offers various options to analyze habit data:
- **Habit Overview**: Get a summary of your habits.
- **Habit Performance**: View performance details of individual habits.
- **Streaks and Consistency**: Analyze streaks and consistency in habit tracking.
- **Categorization Analysis**: Categorize habits and view statistics.
- **Time Analysis**: Analyze habits over time.


### 5. Account Settings

In the Account Settings screen, users can update their personal information:
- **Name**: Update your full name.
- **Username**: Change your username.
- **Email**: Update your email address.
- **New Password**: Set a new password.
- **Confirm New Password**: Confirm the new password.

A "Update" button at the bottom submits the changes.


### Summary

The Habit Tracker application provides a user-friendly interface for managing habits, analyzing progress, and updating account settings. The various screens are designed to guide users through the essential functions of the application, from registering and logging in to managing and analyzing their habits. Each screen is equipped with clear labels and buttons to ensure a smooth user experience.

---

Note: The project includes a `.gitignore` file to exclude unnecessary files and directories from being committed to the repository.

