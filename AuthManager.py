import bcrypt
import os
import threading

class AuthManager:
    def __init__(self, file_path):
        self.file = file_path
        self.lock = threading.Lock()
        self.file_check()

    def file_check(self):
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                pass

    def user_exists(self, username: str) -> bool:
        try:
            with self.lock, open(self.file, "r") as file:
                for line in file:
                    if line.strip().split(":")[0] == username:
                        return True
        except IOError as e:
            print(f"Error reading file: {e}")
        return False

    def sign_up(self, username: str, password: str) -> bool:
        if self.user_exists(username):
            return False

        if not self.is_strong_password(password):
            print("Password too weak.")
            return False

        try:
            password_bytes = password.encode('utf-8')
            hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

            with self.lock, open(self.file, "a") as file:
                file.write(f"{username}:{hashed_pw.decode()}\n")

            return True
        except IOError as e:
            print(f"Error writing file: {e}")
            return False

    def log_in(self, username: str, password: str) -> bool:
        try:
            with self.lock, open(self.file, "r") as file:
                for line in file:
                    credentials = line.strip().split(":")
                    if username == credentials[0]:
                        stored_hash = credentials[1].encode('utf-8')
                        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except IOError as e:
            print(f"Error reading file: {e}")
        return False

    def is_strong_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c.isupper() for c in password):
            return False
        return True
