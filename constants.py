# constants.py

"""
This module contains global constants used throughout the application.
These constants include version information, configuration flags, file paths,
and directory paths for various resources such as databases, fonts, and images.
"""

import os
from typing import List

# Application metadata
VERSION_NR: str = "0.0.1"
"""The version number of the application."""

APP_TITLE: str = "neue App"
"""The title of the application."""
APP_BG: List[float] = [0.1, 0.1, 0.1, 1]
POP_TITLE: List[float] = [0.1, 0.1, 0.8, 1]
POP_SEPARATOR: List[float] = [0.1, 0.1, 0.4, 1]
# Configuration flags
CONFIG_STAT: bool = False
"""A flag indicating the status of the configuration (True if configured, False otherwise)."""

USER_MANAGEMENT: bool = True
"""A flag indicating whether user management is enabled in the application."""

# Data base paths
BASE_DATA: str = os.path.join(os.path.dirname(__file__), "data/base/base_data.json")
"""Path to the base JSON data file."""

BASE_TXT: str = os.path.join(os.path.dirname(__file__), "data/base/base_txt.json")
"""Path to the base text JSON file."""

DATA_APP: str = os.path.join(os.path.dirname(__file__), "data/app/app_data.json")
"""Path to the application-specific JSON data file."""

TXT_APP: str = os.path.join(os.path.dirname(__file__), "data/app/app_txt.json")
"""Path to the application-specific text JSON file."""

USERS_DATA: str = os.path.join(os.path.dirname(__file__), "data/users/user_data.json")
"""Path to the user data JSON file."""

# Directory paths
DIR_USERFILES: str = os.path.join(os.path.dirname(__file__), "data/users/userfiles/")
"""Directory containing user-specific files."""

DIR_FONTS: str = os.path.join(os.path.dirname(__file__), "data/base/base_fonts/")
"""Directory containing font files."""

DIR_FLAGS: str = os.path.join(os.path.dirname(__file__), "data/base/base_images/")
"""Directory containing flag images."""

DIR_POPS: str = os.path.join(os.path.dirname(__file__), "app/ui/popups/")
"""Directory containing popup-related resources."""

LIST_KV_FILES: List[str] = [
    "app/my_widgets/colored_boxlayout.kv",
    "app/my_widgets/themed_widgets.kv",
    "app/my_widgets/own_widgets.kv",
    "app/ui/pages/page_main_scr.kv",
    "app/ui/pages/page_sett_scr.kv",
]
"""List of paths to KV files used in the application."""

SPL_SCREEN_START_APP: str = os.path.join(
    os.path.dirname(__file__), "data/base/base_images/spl_start.png"
)
"""Path to the splash screen image displayed at the start of the application."""

PATH_TO_MAINLOGO_D: str = os.path.join(os.path.dirname(__file__), "data/base/base_images/logo_main_d.png")
"""Path to the main logo image of the application."""
PATH_TO_MAINLOGO_L: str = os.path.join(os.path.dirname(__file__), "data/base/base_images/logo_main_l.png")
"""Path to the main logo image of the application."""