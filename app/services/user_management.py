# user_management.py

from constants import DATA_USERS

import bcrypt
import json
import os


class UserManager:
    def __init__(self):
        self.data_file = DATA_USERS
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            self._create_default_data()

        with open(self.data_file, "r") as f:
            return json.load(f)

    def _save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def _create_default_data(self):
        default = {
            "user_stat": False,
            "login_stat": False,
            "users": {},
        }
        self.data = default
        self._save_data()

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, username: str, password: str) -> bool:
        if username not in self.data["users"]:
            return False
        stored_hash = self.data["users"][username].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

    def add_new_user_to_list(self, username: str, hashed_pw: str):
        if username in self.data["users"]:
            raise ValueError("Benutzername existiert bereits")

        self.data["users"][username] = hashed_pw
        self._save_data()

    def change_user_stat(self, new_user_stat):
        self.data["user_stat"] = new_user_stat
        self._save_data()

    def change_login_state(self, new_login_state: bool):
        self.data["login_stat"] = new_login_state
        self._save_data()
