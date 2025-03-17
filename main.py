# main.py
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

# Import data_manager
from app.services.data_manager import read_from_json
from app.services.user_manager import UserManager
from app.services.popup_manager import PopupManager

# Import pages
from app.ui.pages.page_load_scr import Page_Load_Scr
from app.ui.pages.page_main_scr import StartPage
from app.ui.pages.page_sett_scr import SettingPage

from app.my_widgets.colored_boxlayout import (
    ColBoxLayout_1,
    ColBoxLayout_2,
    ColBoxLayout_3,
    ColoredBoxLayoutBase,
)
from app.services.theme_manager import ThemeManager
from app.my_widgets.themed_widgets import Lbl_Big, Btn_Clear  # Pfad anpassen!

# Load all KV files
for kv_file in LIST_KV_FILES:
    Builder.load_file(kv_file)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Sicherheit: theme_manager als Instanzattribut initialisieren
        self.base_data, self.base_txt, self.users_data = {}, {}, {}
        self.load_app_data()
        if not hasattr(self, "theme_manager"):
            self.theme_manager = ThemeManager()
        self.popup_manager = PopupManager()
        # Optional: Standard-Theme setzen
        if USER_MANAGEMENT:
            self.user_manager = UserManager()


        
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

        Adds the initial screens (Page_Load_Scr, StartPage, and SettingPage) to the ScreenManager.

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

        # Erstelle die StartPage
        self.start_page = Screen(name="page_start")
        self.start_page.add_widget(StartPage())
        self.scr_man.add_widget(self.start_page)
        Clock.schedule_once(lambda dt: self.start_page.children[0].upd_page(), 0)

        # Erstelle die SettingPage
        self.setting_page = Screen(name="page_setting")
        self.setting_page.add_widget(SettingPage(app))
        self.scr_man.add_widget(self.setting_page)

        Clock.schedule_once(self._apply_initial_theme, 0)

        return self.scr_man

    def _apply_initial_theme(self, *args):
        """Rekursiv alle Widgets durchsuchen und Theme anwenden"""
        root = self.root
        if root:
            self._traverse_widgets(root, self._update_theme_colors)

    def _traverse_widgets(self, widget, callback):
        """Rekursive Widget-Traversal"""
        callback(widget)
        for child in widget.children:
            self._traverse_widgets(child, callback)

    def _update_theme_colors(self, widget):
        """Theme-Update für kompatible Widgets"""
        if hasattr(widget, "update_theme_colors"):
            widget.update_theme_colors()

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

    def change_theme(self, theme_name):
        self.theme_manager.change_theme(theme_name)

    def load_app_data(self) -> None:
        """
        load base data in the app.

        Loads the colors and text data, and converts color values from 0-255 to 0-1 range.
        """
        # Store the loaded colors as instance variables
        self.base_data = read_from_json(DATA_BASE)
        self.base_txt = read_from_json(TXT_BASE)[self.base_data["curr_lang"]]
        self.users_data = read_from_json(DATA_USERS)

    def start_user_management(self):
        """
        If USER_MANAGEMENT == True, user management is activated and this function
        controls which user status is active and opens the corresponding pop-up.

        Returns: None
        """
        if not self.users_data["user_stat"]:
            self.popup_manager.open_usr_man_pop("register")
        elif not self.users_data["login_stat"]:
            self.popup_manager.open_usr_man_pop("login")

    def get_user_manager(self) -> "UserManager":
        """
        Provides access to the user management system for cross-module usage.

        This getter method ensures controlled access to the user manager instance,
        which handles authentication, user data storage, and session management.

        Returns:
            UserManager: Singleton instance coordinating user-related operations
        """
        return self.user_manager

    def get_popup_manager(self) -> "PopupManager":
        """
        Provides access to the popup management system for cross-module usage.

        This getter method ensures controlled access to the user manager instance,
        which handles authentication, user data storage, and session management.

        Returns:
            UserManager: Singleton instance coordinating user-related operations
        """
        return self.popup_manager

    def on_start(self):
        """Wird aufgerufen, nachdem die App vollständig initialisiert ist"""
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
            self.user_manager.change_stat("login_stat", False)


if __name__ == "__main__":
    app = MainApp()
    app.run()
