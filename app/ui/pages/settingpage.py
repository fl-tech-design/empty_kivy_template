# settingpage.py
from constants import DIR_FLAGS

from typing import Any, Dict

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock

from app.services.contr_str import let_upper_first
from app.services.contr_data import update_base_data


class SettingPage(Screen):
    def __init__(self, app: App, **kwargs: Dict[str, Any]) -> None:
        """
        Initialize the SettingPage screen.

        :param app: The main application instance.
        :param kwargs: Additional keyword arguments.
        """
        super(SettingPage, self).__init__(**kwargs)
        self.app = app
        self.ids.box_flag_1.ids.img_flag.source = DIR_FLAGS + "flag_germany.png"
        self.ids.box_flag_2.ids.img_flag.source = DIR_FLAGS + "flag_uk.png"
        self.ids.box_flag_1.ids.lab_but_flag.bind(
            on_release=lambda instance: self.change_language(instance.text.lower())
        )
        self.ids.box_flag_2.ids.lab_but_flag.bind(
            on_release=lambda instance: self.change_language(instance.text.lower())
        )

    def upd_page(self, *args: Any) -> None:
        """
        Update the text elements on the settings page based on the application's base text data.
        """
        self.upd_labels()

    def upd_labels(self):
        """
        Updates all labeltextes of this page
        Returns: None
        """
        self.ids.t_box_sett.ids.lab_tit_page.text = self.app.base_txt["tit_page_sett"]
        self.ids.lab_tit_lang.text = self.app.base_txt["languages"]
        self.ids.box_flag_1.ids.lab_but_flag.text = let_upper_first(
            self.app.base_txt["german"]
        )
        self.ids.box_flag_2.ids.lab_but_flag.text = let_upper_first(
            self.app.base_txt["english"]
        )
        self.ids.b_box_settings.ids.but_1.text = let_upper_first(
            self.app.base_txt["back"]
        )
        self.ids.b_box_settings.ids.but_2.text = let_upper_first(
            self.app.base_txt["exit"]
        )
        self.ids.lbl_add_new_user.text = self.app.base_txt["new_user"]
        self.ids.btn_add_new_user.text = self.app.base_txt["add"]

    def change_language(self, new_language: str) -> None:
        """
        Change the application's language setting and update the page accordingly.

        :param new_language: The new language to set (e.g., "German" or "English").
        """
        if new_language == self.app.base_txt["german"]:
            update_base_data("curr_lang", "de")
        elif new_language == self.app.base_txt["english"]:
            update_base_data("curr_lang", "en")
        self.app.load_app_data()
        Clock.schedule_once(self.upd_page)
        # new_screen = self.scr_man.get_screen("page_setting")
        # Clock.schedule_once(lambda dt: new_screen.children[0].upd_page(), 0)
