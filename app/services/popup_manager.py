# popup_manager.py
from typing import Any, Dict

from kivy.app import App

from app.ui.popups.pop_info import Pop_Info
from app.ui.popups.pop_auth_user import Pop_Auth_User
from app.ui.popups.pop_error import Pop_Error


class PopupManager:
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """
        Initialize the Page_Settings screen.

        :param app: The main application instance
        :param kwargs: Additional keyword arguments for Kivy
        """
        super(PopupManager, self).__init__(**kwargs)
        self.app = App.get_running_app()  # Holt die MainApp-Instanz

    def open_inf_pop(self, screen_name: str, *args):
        if screen_name == "page_start":
            message = self.app.base_txt["inf_start"]
        elif screen_name == "page_setting":
            message = self.app.base_txt["inf_settings"]

        popup_content = message
        popup = Pop_Info(info_msg=popup_content)
        popup.open()

    def open_usr_man_pop(self, popup_stat: str, *args):
        popup = Pop_Auth_User(popup_stat)
        popup.open()

    def open_error_popup(self, message, *args):
        popup_content = message
        dynamic_popup = Pop_Error(err_msg=popup_content)
        dynamic_popup.open()
