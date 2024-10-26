Sure, here is the complete User Interface Overview for your GitHub README, including the "Load Test Data" button:

---

# Habit Tracker

Habit Tracker is a Python application that helps you develop and maintain good habits. It allows you to create, track, and analyze your habits, providing a comprehensive solution for personal growth and self-improvement.

## How To Get Started

### Dependencies

- Python 3.7+

Sure, here are the updated installation instructions, including steps for Windows users, and instructions for installing `pip` and `brew` if they are not already installed:

### Installation Instructions

#### Prerequisites

1. **Install Homebrew (for macOS users)**:
    - Open Terminal and run:
      ```sh
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```

2. **Install pip (if not already installed)**:
    - **Windows**:
      - Download `get-pip.py` from [here](https://bootstrap.pypa.io/get-pip.py).
      - Open Command Prompt and run:
        ```sh
        python get-pip.py
        ```
    - **macOS/Linux**:
      - Open Terminal and run:
        ```sh
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py
        ```

#### Project Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/KatLutgen/HabitTrackerIU.git
    ```

2. **Navigate to the project directory**:
    ```sh
    cd HabitTrackerIU
    ```

3. **Install `Tcl/Tk` libraries**:
    - **macOS**:
      ```sh
      brew install python-tk
      ```
    - **Windows**:
      - `tkinter` is usually included with Python. If not, download and install the latest version of Python from [python.org](https://www.python.org/downloads/).

4. **Create and activate a virtual environment**:
    - **macOS/Linux**:
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```
    - **Windows**:
      ```sh
      python -m venv venv
      venv\Scripts\activate
      ```

5. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Notes:
- Ensure you have Git installed. If not, download it from [git-scm.com](https://git-scm.com/downloads).
- The `Tcl/Tk` installation step for Windows users is usually unnecessary as `tkinter` comes bundled with the standard Python installer. If any issues arise, ensure you are using the latest Python version.


### Run The Application

To start the Habit Tracker application, run the following command:
```sh
python3 main/main.py
```


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

