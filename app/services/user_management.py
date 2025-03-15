# user_management.py

from constants import DATA_USERS

import bcrypt
import json
import os


import os
import json
import bcrypt
from typing import Dict, Any

class UserManager:
    def __init__(self):
        """
        Initializes the user manager with configuration data.
        
        Loads user data from the configured JSON file, creates default
        data structure if the file doesn't exist.
        """
        self.data_file: str = DATA_USERS  # Path to user data file
        self.data: Dict[str, Any] = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """
        Loads user data from the configured JSON file.
        
        Creates default data if the file doesn't exist. Should only be
        called during initialization.

        Returns:
            Dict[str, Any]: Loaded user data structure
        """
        if not os.path.exists(self.data_file):
            self._create_default_data()

        with open(self.data_file, "r") as f:
            return json.load(f)

    def _save_data(self) -> None:
        """
        Persists current user data to the JSON file.
        
        Writes the entire data structure to disk with indentation
        for human readability.
        """
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def _create_default_data(self) -> None:
        """
        Creates initial default user data structure.
        
        Defines the base structure containing:
        - user_stat (bool)
        - login_stat (bool)
        - users (Dict[str, str])
        """
        default: Dict[str, Any] = {
            "user_stat": False,
            "login_stat": False,
            "users": {},
        }
        self.data = default
        self._save_data()

    def hash_password(self, password: str) -> str:
        """
        Creates a bcrypt password hash.
        
        Uses bcrypt's salted hashing mechanism for secure password storage.

        Args:
            password: Plain text password to hash

        Returns:
            str: Base64-encoded password hash
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, username: str, password: str) -> bool:
        """
        Verifies password against stored hash.
        
        Checks if the user exists and the password matches the stored hash.

        Args:
            username: User to verify
            password: Plain text password to check

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if username not in self.data["users"]:
            return False
        stored_hash = self.data["users"][username].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

    def add_new_user_to_list(self, username: str, hashed_pw: str) -> None:
        """
        Registers a new user in the system.
        
        Validates username uniqueness before adding to the user list.

        Args:
            username: New user's unique identifier
            hashed_pw: Pre-hashed password string

        Raises:
            ValueError: If username already exists
        """
        if username in self.data["users"]:
            raise ValueError("Username already exists")
        self.data["users"][username] = hashed_pw
        self._save_data()

    def change_user_stat(self, new_user_stat: bool) -> None:
        """
        Updates the user management status.
        
        Persists the change to the configuration file immediately.

        Args:
            new_user_stat: New status value to set
        """
        self.data["user_stat"] = new_user_stat
        self._save_data()

    def change_login_state(self, new_login_state: bool) -> None:
        """
        Updates the login status.
        
        Persists the change to the configuration file immediately.

        Args:
            new_login_state: New login status value to set
        """
        self.data["login_stat"] = new_login_state
        self._save_data()