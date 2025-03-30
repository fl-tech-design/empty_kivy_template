"""
This module defines the Page_Settings screen, which allows users to configure application settings,
such as language selection, theme management, and user data handling.
"""

from constants import (
    DIR_IMGS,
    DIR_USERFILES,
    USER_MANAGEMENT,
    PATH_TO_MAINLOGO_D,
    PATH_TO_MAINLOGO_L,
)

from typing import Any, Dict
import os

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from app.services.contr_str import let_up_first
from app.services.data_manager import update_base_data


class Page_Settings(Screen):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """
        Initialize the Page_Settings screen.

        Args:
            app: The main application instance.
            **kwargs: Additional keyword arguments for Kivy.
        """
        super(Page_Settings, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.logger = self.app.logger
        self.change_but_disabled()
        self.btn_binds()

        if USER_MANAGEMENT:
            self.usr_man = self.app.get_usr_man()

        self.pop_man = self.app.get_pop_man()

    def upd_page(self, *args: Any) -> None:
        """
        Update all dynamic content on the settings page.

        This method refreshes text elements and UI components based on the current
        application state and language settings. Should be called after language
        changes or configuration updates.
        """
        self.set_img_sources()
        self.upd_labels()

    def upd_labels(self) -> None:
        """
        Refresh all text elements on the page.

        Updates labels and buttons according to the current language settings
        stored in the application's base_txt dictionary.
        """
        base_txt = self.app.base_txt
        self.ids.t_box_sett.ids.lab_tit_page.text = let_up_first(base_txt["settings"])
        self.ids.lab_tit_lang.text = self.app.base_txt["languages"]
        self.ids.b_flag_1.ids.but_flag.text = let_up_first(base_txt["german"])
        self.ids.b_flag_2.ids.but_flag.text = let_up_first(base_txt["english"])
        self.ids.b_flag_3.ids.but_flag.text = let_up_first(base_txt["french"])
        self.ids.b_flag_4.ids.but_flag.text = let_up_first(base_txt["italian"])
        self.ids.b_flag_5.ids.but_flag.text = let_up_first(base_txt["spanish"])
        self.ids.b_box_settings.ids.but_1.text = let_up_first(base_txt["back"])
        self.ids.b_box_settings.ids.but_2.text = let_up_first(base_txt["exit"])
        self.ids.lab_tit_usr_man.text = let_up_first(base_txt["user_management"])

        self.ids.lbl_add_new_user.text = let_up_first(base_txt["new_user"])
        self.ids.btn_add_new_user.text = let_up_first(base_txt["add"])
        self.ids.lbl_res_u_data.text = base_txt["res_u_data"]
        self.ids.btn_res_u_data.text = let_up_first(base_txt["delete"])

    def change_lang(self, new_language: str) -> None:
        """
        Handle language change requests.

        Updates the application's language configuration and refreshes the UI
        to reflect the new language setting.

        Args:
            new_language (str): Language code to switch to (e.g., "de" or "en").
        """
        if new_language == self.app.base_txt["german"]:
            update_base_data("curr_lang", "de")
        elif new_language == self.app.base_txt["english"]:
            update_base_data("curr_lang", "en")
        elif new_language == self.app.base_txt["french"]:
            update_base_data("curr_lang", "fr")
        elif new_language == self.app.base_txt["italian"]:
            update_base_data("curr_lang", "it")
        elif new_language == self.app.base_txt["spanish"]:
            update_base_data("curr_lang", "es")
        self.app.load_app_data()
        Clock.schedule_once(self.upd_page)

    def add_new_user(self) -> None:
        """
        Add a new user to the application.

        Resets the user status to allow registration and triggers the user management process.
        """
        self.usr_man.change_stat("user_stat", False)
        self.app.load_app_data()
        self.app.start_user_management()

    def reset_userdata(self) -> None:
        """
        Reset all user data to the initial state.

        Performs two main actions:
        1. Deletes all individual user JSON files in DIR_USERFILES.
        2. Resets the main user management data to default values.

        Note:
            This is a destructive operation that:
            - Removes all user accounts.
            - Deletes all user-specific data files.
            - Resets login and user management status.
        """
        try:
            for filename in os.listdir(DIR_USERFILES):
                if filename.endswith(".json"):
                    file_path = os.path.join(DIR_USERFILES, filename)
                    try:
                        os.remove(file_path)
                        self.logger.info(f"Deleted user file: {file_path}")
                    except Exception as e:
                        self.logger.error(f"Failed to delete {file_path}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to access user files directory: {e}")

        try:
            self.usr_man._create_default_data()
            self.logger.info("User management data reset to default state")
        except Exception as e:
            self.logger.error(f"Failed to reset user management data: {e}")

        self.app.load_app_data()
        self.app.change_screen("right", "page_start")
        self.app.start_user_management()

    def btn_binds(self, *args) -> None:
        """
        Binds button actions to their respective event handlers.

        This method ensures that buttons on the Page_Start screen are connected to
        their corresponding popup or action logic.
        """
        self.ids.b_flag_1.ids.but_flag.bind(
            on_release=lambda instance: self.change_lang(instance.text.lower())
        )
        self.ids.b_flag_2.ids.but_flag.bind(
            on_release=lambda instance: self.change_lang(instance.text.lower())
        )
        self.ids.b_flag_3.ids.but_flag.bind(
            on_release=lambda instance: self.change_lang(instance.text.lower())
        )
        self.ids.b_flag_4.ids.but_flag.bind(
            on_release=lambda instance: self.change_lang(instance.text.lower())
        )
        self.ids.b_flag_5.ids.but_flag.bind(
            on_release=lambda instance: self.change_lang(instance.text.lower())
        )
        # Bind info button to open popup
        self.ids.t_box_sett.ids.but_info.bind(
            on_release=lambda instance: self.app.get_pop_man().open_inf_pop(
                "page_setting"
            )
        )

    def set_img_sources(self):
        # Set flag images and bind language change actions
        self.ids.b_flag_1.ids.img_flag.source = os.path.join(DIR_IMGS, "flag_ger.png")
        self.ids.b_flag_2.ids.img_flag.source = os.path.join(DIR_IMGS, "flag_eng.png")
        self.ids.b_flag_3.ids.img_flag.source = os.path.join(DIR_IMGS, "flag_fra.png")
        self.ids.b_flag_4.ids.img_flag.source = os.path.join(DIR_IMGS, "flag_ita.png")
        self.ids.b_flag_5.ids.img_flag.source = os.path.join(DIR_IMGS, "flag_spa.png")
        if self.app.theme_manager.current_theme == "dark":
            self.ids.t_box_sett.ids.img_logo_main.source = PATH_TO_MAINLOGO_D
        else:
            self.ids.t_box_sett.ids.img_logo_main.source = PATH_TO_MAINLOGO_L

    def change_but_disabled(self):
        if USER_MANAGEMENT:
            self.ids.btn_add_new_user.disabled = False
            self.ids.btn_res_u_data.disabled = False
        else:
            self.ids.btn_add_new_user.disabled = True
            self.ids.btn_res_u_data.disabled = True
