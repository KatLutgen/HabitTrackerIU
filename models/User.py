from datetime import datetime
import bcrypt

class User:
    def __init__(self, name, username, password, email=None, profile_picture=None):
        self.user_id = None
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.account_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None
        self.status = "Active"
        self.profile_picture = profile_picture


    def set_last_login(self):
        self.last_login = datetime.now()

    def reset(self, reset_type: int):
        if reset_type == 1:
            self.last_login = self.account_created
        elif reset_type == 2:
            self.status = "Active"
        elif reset_type == 3:
            self.profile_picture = ""
        else:
            print("Invalid reset type specified.")

    def info(self) -> str:
        return f"User ID: {self.user_id}, Name: {self.name}, Username: {self.username}"

    def auth(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def update_password(self, new_password):
        self.password = new_password

    def update_email(self, new_email: str):
        self.email = new_email
