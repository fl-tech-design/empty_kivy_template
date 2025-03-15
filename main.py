# main.py
# Import constants from constants.py
from constants import (
    LIST_KV_FILES,
    SPL_SCREEN_START_APP,
    DATA_BASE,
    TXT_BASE,
    DATA_USERS,
    APP_TITLE,
    CONFIG_STAT,
    USER_MANAGEMENT,
)

## configuration of kivy
from kivy.config import Config


def config_win_size(h: str = "850", w: str = "850") -> None:
    """
    Configure Kivy window dimensions and resizable state.

    Sets the initial window size and enables/disables resizing capability.
    Must be called BEFORE creating the App instance to take effect.
    Configuration is persisted to the Kivy config file.

    Args:
        h (str): Window height in pixels (default: "850")
        w (str): Window width in pixels (default: "850")

    Example:
        config_win_size("1080", "1920")  # Sets 1920x1080 window
    """
    Config.set("graphics", "resizable", "1")
    Config.set("graphics", "height", h)
    Config.set("graphics", "width", w)
    Config.write()


if CONFIG_STAT:
    config_win_size()

# Imports of basic packages

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

# Import DataControl
from app.services.data_services import read_from_json

from app.services.user_management import UserManager

# Import pages
from app.ui.pages.loadingpage import LoadingPage
from app.ui.pages.startpage import StartPage
from app.ui.pages.settingpage import SettingPage


from app.ui.popups.pop_info import Pop_Info
from app.ui.popups.pop_auth_user import Pop_Auth_User


# Load all KV files
for kv_file in LIST_KV_FILES:
    Builder.load_file(kv_file)


class MainApp(App):
    def build(self) -> ScreenManager:
        """
        Builds the main application interface.

        Initializes the DataControl, loads data, and sets up the ScreenManager.

        Returns:
            ScreenManager: The main ScreenManager for the application.
        """
        global app
        app = self
        self.title = APP_TITLE

        # Initialize DataControl and load JSON data
        self.base_data, self.base_txt = {}, {}
        self.users_data = {}
        self.color1, self.color2, self.color3 = [], [], []
        self.load_app_data()

        # Initialize the UserManager
        if USER_MANAGEMENT:
            self.user_manager = UserManager()
            self.start_user_management()

        # Initialize the ScreenManager
        self.scr_man = ScreenManager()
        return self._create_screen_manager()

    def _create_screen_manager(self) -> ScreenManager:
        """
        Creates and configures the ScreenManager.

        Adds the initial screens (LoadingPage, StartPage, and SettingPage) to the ScreenManager.

        Returns:
            ScreenManager: The configured ScreenManager.
        """
        # Create the LoadingPage
        self.spl_scr_start = LoadingPage(
            app,
            self.base_txt,
            self.scr_man,
            SPL_SCREEN_START_APP,
            "page_start",
            name="spl_scr_start",
        )
        self.scr_man.add_widget(self.spl_scr_start)

        # Erstelle die StartPage
        self.start_page = Screen(name="page_start")
        self.start_page.add_widget(StartPage(app))
        self.scr_man.add_widget(self.start_page)
        Clock.schedule_once(lambda dt: self.start_page.children[0].upd_page(), 0)

        # Erstelle die SettingPage
        self.setting_page = Screen(name="page_setting")
        self.setting_page.add_widget(SettingPage(app))
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

    def load_app_data(self) -> None:
        """
        load base data in the app.

        Loads the colors and text data, and converts color values from 0-255 to 0-1 range.
        """
        # Store the loaded colors as instance variables
        self.base_data = read_from_json(DATA_BASE)
        self.base_txt = read_from_json(TXT_BASE)[self.base_data["curr_lang"]]
        self.users_data = read_from_json(DATA_USERS)
        self.color1 = [c / 255 for c in self.base_data["colors"]["color1"]]
        self.color2 = [c / 255 for c in self.base_data["colors"]["color2"]]
        self.color3 = [c / 255 for c in self.base_data["colors"]["color3"]]

    def open_inf_pop(self, *args):
        if self.scr_man.current == "page_start":
            inf_msg = self.base_txt["inf_start"]
        elif self.scr_man.current == "page_setting":
            inf_msg = self.base_txt["inf_settings"]
        popup = Pop_Info(app, inf_msg)
        popup.open()

    def start_user_management(self):
        """
        If USER_MANAGEMENT == True, user management is activated and this function
        controls which user status is active and opens the corresponding pop-up.

        Returns: None
        """
        if not self.users_data["user_stat"]:
            create_user_popup = Pop_Auth_User(app, "register")
            create_user_popup.open()
        elif not self.users_data["login_stat"]:
            login_user_popup = Pop_Auth_User(app, "login")
            login_user_popup.open()

    def get_user_manager(self) -> "UserManager":
        """
        Provides access to the user management system for cross-module usage.

        This getter method ensures controlled access to the user manager instance,
        which handles authentication, user data storage, and session management.

        Returns:
            UserManager: Singleton instance coordinating user-related operations
        """
        return self.user_manager

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
            self.user_manager.change_stat("login_stat",False)


if __name__ == "__main__":
    app = MainApp()
    app.run()
