import sys
import os
import logging

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from database.db_manager import DBManager



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='habit_tracker.log', filemode='a')

logging.info("User logged in successfully.")
logging.warning("User not found in the database.")

def main():
    try:
        DBManager.initialize_database()
        logging.info("Database initialized successfully.")
        from ui.Gui import start_screen, root
        start_screen()
        root.mainloop()  # Add this line to start the main event loop
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")


if __name__ == "__main__":
    main()