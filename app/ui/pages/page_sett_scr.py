# settingpage.py
from typing import Any, Dict
import os
from app.services.logger_config import setup_logger

logger = setup_logger()

from constants import DIR_FLAGS, DIR_USERFILES, USER_MANAGEMENT


from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from app.services.contr_str import let_up_first
from app.services.data_manager import update_base_data


class SettingPage(Screen):
    def __init__(self, app, **kwargs: Dict[str, Any]) -> None:
        """
        Initialize the SettingPage screen.

        :param app: The main application instance
        :param kwargs: Additional keyword arguments for Kivy
        """
        super(SettingPage, self).__init__(**kwargs)
        self.app = app
        Clock.schedule_once(lambda *args: self.ids.box_flag_1.update_theme_colors())        
        
        if USER_MANAGEMENT:
            self.usr_man = self.app.get_user_manager()
        self.pop_man = self.app.get_popup_manager()

        self.ids.box_flag_1.ids.img_flag.source = DIR_FLAGS + "flag_germany.png"
        self.ids.box_flag_2.ids.img_flag.source = DIR_FLAGS + "flag_uk.png"
        self.ids.box_flag_1.ids.lab_but_flag.bind(
            on_release=lambda instance: self.change_language(instance.text.lower())
        )
        self.ids.box_flag_2.ids.lab_but_flag.bind(
            on_release=lambda instance: self.change_language(instance.text.lower())
        )

        self.ids.t_box_sett.ids.but_info.bind(
            on_release=lambda instance: self.app.get_popup_manager().open_inf_pop(
                "page_setting"
            )
        )

    def upd_page(self, *args: Any) -> None:
        """
        Update all dynamic content on the settings page.

        This method refreshes text elements and UI components based on the current
        application state and language settings. Should be called after language
        changes or configuration updates.
        """
        self.upd_labels()

    def upd_labels(self) -> None:
        """
        Refresh all text elements on the page.

        Updates labels and buttons according to the current language settings
        stored in the application's base_txt dictionary.
        """
        self.ids.t_box_sett.ids.lab_tit_page.text = self.app.base_txt["tit_page_sett"]
        self.ids.lab_tit_lang.text = self.app.base_txt["languages"]
        self.ids.box_flag_1.ids.lab_but_flag.text = let_up_first(
            self.app.base_txt["german"]
        )
        self.ids.box_flag_2.ids.lab_but_flag.text = let_up_first(
            self.app.base_txt["english"]
        )
        self.ids.b_box_settings.ids.but_1.text = let_up_first(self.app.base_txt["back"])
        self.ids.b_box_settings.ids.but_2.text = let_up_first(self.app.base_txt["exit"])
        self.ids.lab_tit_usr_man.text = let_up_first(
            self.app.base_txt["user_management"]
        )

        self.ids.lbl_add_new_user.text = self.app.base_txt["new_user"]
        self.ids.btn_add_new_user.text = let_up_first(self.app.base_txt["add"])
        self.ids.lbl_res_u_data.text = self.app.base_txt["res_u_data"]
        self.ids.btn_res_u_data.text = let_up_first(self.app.base_txt["delete"])

    def change_language(self, new_language: str) -> None:
        """
        Handle language change requests.

        Updates the application's language configuration and refreshes the UI
        to reflect the new language setting.

        :param new_language: Language code to switch to (e.g., "de" or "en")
        """
        if new_language == self.app.base_txt["german"]:
            update_base_data("curr_lang", "de")
        elif new_language == self.app.base_txt["english"]:
            update_base_data("curr_lang", "en")
        self.app.load_app_data()
        Clock.schedule_once(self.upd_page)

    def add_new_user(self):
        self.usr_man.change_stat("user_stat", False)
        self.app.load_app_data()
        self.app.start_user_management()

    def reset_userdata(self) -> None:
        """
        Resets all user data to initial state.

        Performs two main actions:
        1. Deletes all individual user JSON files in DIR_USERFILES
        2. Resets the main user management data to default values

        Note:
            This is a destructive operation that:
            - Removes all user accounts
            - Deletes all user-specific data files
            - Resets login and user management status
        """
        try:
            for filename in os.listdir(DIR_USERFILES):
                if filename.endswith(".json"):
                    file_path = os.path.join(DIR_USERFILES, filename)
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted user file: {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete {file_path}: {e}")
        except Exception as e:
            logger.error(f"Failed to access user files directory: {e}")

        try:
            self.usr_man._create_default_data()
            logger.info("User management data reset to default state")
        except Exception as e:
            logger.error(f"Failed to reset user management data: {e}")
        self.app.load_app_data()
        self.app.change_screen("right", "page_start")
        self.app.start_user_management()
