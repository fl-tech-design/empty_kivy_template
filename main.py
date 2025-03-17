"""
Main entry point for the Kivy application.

This script initializes the application, loads necessary resources,
and manages the main application logic, including screen management,
theme handling, and user management.
"""

from constants import (
    LIST_KV_FILES,
    SPL_SCREEN_START_APP,
    BASE_DATA,
    BASE_TXT,
    USERS_DATA,
    APP_TITLE,
    USER_MANAGEMENT,
)

# Import configuration setup
from app.services.app_config import start_app_config

start_app_config()

# Imports of basic packages
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

# Import data_manager
from app.services.data_manager import read_from_json
from app.services.user_manager import UserManager
from app.services.popup_manager import PopupManager
from app.services.theme_manager import ThemeManager
from app.services.logger_config import setup_logger

# Import pages
from app.ui.pages.page_load_scr import Page_Load_Scr
from app.ui.pages.page_main_scr import Page_Start
from app.ui.pages.page_sett_scr import Page_Settings

# Import custom widgets
# These imports are required for Kivy to register the custom widgets used in .kv files.
# Even though they are not directly used in this file, removing them will cause a FactoryException.
from app.my_widgets.colored_boxlayout import (
    ColBoxLayout_1,
    ColBoxLayout_2,
    ColBoxLayout_3,
    ColBoxLayout_4,
    ColBoxLayout_5,
    ColoredBoxLayoutBase,
)
from app.my_widgets.themed_widgets import Lbl_Big, Btn_Clear  # Required for dynamic widget creation in .kv files


# Load all KV files
for kv_file in LIST_KV_FILES:
    Builder.load_file(kv_file)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = setup_logger()
        self.base_data: dict = {}
        self.base_txt: dict = {}
        self.users_data: dict = {}
        self.load_app_data()

        if not hasattr(self, "theme_manager"):
            self.theme_manager = ThemeManager()
        if not hasattr(self, "popup_manager"):
            self.popup_manager = PopupManager()
        if USER_MANAGEMENT:
            self.usr_man = UserManager()

    def build(self) -> ScreenManager:
        """
        Builds the main application interface.

        Initializes the data_manager, loads data, and sets up the ScreenManager.

        Returns:
            ScreenManager: The main ScreenManager for the application.
        """
        self.title = APP_TITLE
        self.scr_man = ScreenManager()
        return self._create_screen_manager()

    def _create_screen_manager(self) -> ScreenManager:
        """
        Creates and configures the ScreenManager.

        Adds the initial screens (Page_Load_Scr, Page_Start, and Page_Settings) to the ScreenManager.

        Returns:
            ScreenManager: The configured ScreenManager.
        """
        # Create the Page_Load_Scr
        self.spl_scr_start = Page_Load_Scr(
            SPL_SCREEN_START_APP,
            "page_start",
            name="spl_scr_start",
        )
        self.scr_man.add_widget(self.spl_scr_start)

        # Create the Page_Start
        self.start_page = Screen(name="page_start")
        self.start_page.add_widget(Page_Start())
        self.scr_man.add_widget(self.start_page)
        Clock.schedule_once(lambda dt: self.start_page.children[0].upd_page(), 0)

        # Create the Page_Settings
        self.setting_page = Screen(name="page_setting")
        self.setting_page.add_widget(Page_Settings())
        self.scr_man.add_widget(self.setting_page)

        return self.scr_man

    def change_screen(self, new_transition: str, new_scr_name: str) -> None:
        """
        Changes the current screen with a specified transition.

        Args:
            new_transition (str): The direction of the transition (e.g., 'left', 'right').
            new_scr_name (str): The name of the screen to switch to.
        """
        self.root.transition.direction = new_transition
        self.root.current = new_scr_name
        new_screen = self.scr_man.get_screen(new_scr_name)
        Clock.schedule_once(lambda dt: new_screen.children[0].upd_page(), 0)

    def change_theme(self, theme_name: str) -> None:
        """
        Changes the application's theme.

        Args:
            theme_name (str): The name of the theme to apply.
        """
        self.theme_manager.change_theme(theme_name)

    def load_app_data(self) -> None:
        """
        Load base data into the app.

        Loads the colors and text data, and converts color values from 0-255 to 0-1 range.
        """
        self.base_data = read_from_json(BASE_DATA)
        self.base_txt = read_from_json(BASE_TXT)[self.base_data["curr_lang"]]
        self.users_data = read_from_json(USERS_DATA)

    def start_user_management(self) -> None:
        """
        If USER_MANAGEMENT == True, user management is activated and this function
        controls which user status is active and opens the corresponding pop-up.

        Returns: None
        """
        if not self.users_data["user_stat"]:
            self.popup_manager.open_usr_man_pop("register")
        elif not self.users_data["login_stat"]:
            self.popup_manager.open_usr_man_pop("login")

    def get_usr_man(self) -> "UserManager":
        """
        Provides access to the user management system for cross-module usage.

        This getter method ensures controlled access to the user manager instance,
        which handles authentication, user data storage, and session management.

        Returns:
            UserManager: Singleton instance coordinating user-related operations
        """
        return self.usr_man

    def get_pop_man(self) -> "PopupManager":
        """
        Provides access to the popup management system for cross-module usage.

        This getter method ensures controlled access to the user manager instance,
        which handles authentication, user data storage, and session management.

        Returns:
            PopupManager: Singleton instance coordinating user-related operations
        """
        return self.popup_manager

    def on_stop(self) -> None:
        """
        Handles application shutdown procedures.

        If user management is enabled (USER_MANAGEMENT = True), this method
        resets the login state through the user manager. Called automatically
        when the Kivy application stops.

        Note:
            Relies on the global USER_MANAGEMENT flag to determine behavior.
        """
        if USER_MANAGEMENT:
            self.usr_man.change_stat("login_stat", False)


if __name__ == "__main__":
    app = MainApp()
    app.run()