from typing import Any
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

from constants import DIR_POPS, USER_MANAGEMENT
from app.services.contr_str import let_up_first
from app.ui.popups.pop_error import Pop_Error

Builder.load_file(DIR_POPS + "pop_auth_user.kv")


class Pop_Auth_User(Popup):
    """Popup for user authentication (login/registration).

    Args:
        mode (str): Operation mode ('login' or 'register')
        **kwargs: Additional keyword arguments for Popup
    """

    def __init__(self, mode: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.app: App = App.get_running_app()
        self.mode: str = mode
        self.usr_man: Any = self.app.get_usr_man() if USER_MANAGEMENT else None
        self.pop_man: Any = self.app.get_pop_man()

        self._update_labels()
        Clock.schedule_once(self.set_focus)
        Window.bind(on_key_down=self.on_key_down)

    def _update_labels(self) -> None:
        """Update all labels based on current mode (login/registration)."""
        base_txt = self.app.base_txt
        mode_title = "create_user" if self.mode == "register" else "login_user"

        self.title = base_txt[mode_title]
        self.ids.lab_inf_create_user.text = base_txt[f"inf_{self.mode}_user"]
        self.ids.inp_username.hint_text = let_up_first(base_txt["username"])
        self.ids.inp_passwd.hint_text = let_up_first(base_txt["password"])
        self.ids.but_confirm.text = let_up_first(base_txt["confirm"])
        self.ids.but_close.text = let_up_first(base_txt["chancel"])

    def but_confirm_released(self) -> None:
        """Handle confirm button release - performs login/registration."""
        username: str = self.ids.inp_username.text.strip()
        password: str = self.ids.inp_passwd.text.strip()
        base_txt: dict = self.app.base_txt

        if not username:
            self.ids.inp_username.hint_text = let_up_first(
                base_txt["pl_enter_a_u_name"]
            )
            return

        if not password:
            self.ids.inp_passwd.hint_text = let_up_first(base_txt["pl_enter_a_pw"])
            return

        try:
            if self.mode == "login":
                if self.usr_man.verify_password(username, password):
                    self.usr_man.change_stat("login_stat", True)
                    self._close_popup()
                else:
                    self.pop_man.open_error_popup(base_txt["inf_err_login"])

            elif self.mode == "register":
                hashed_pw: str = self.usr_man.hash_password(password)
                self.usr_man.add_new_user_to_list(username, hashed_pw)
                self.usr_man.change_stat("user_stat", True)
                self.usr_man.change_stat("login_stat", True)
                self._close_popup()

        except Exception as e:
            self.pop_man.open_error_popup(base_txt["inf_err_regist"])

    def on_key_down(
        self, window: Any, key: int, scancode: int, codepoint: str, modifier: list
    ) -> bool:
        """Handle keyboard input (TAB key for focus switching).

        Args:
            window: Kivy window instance
            key (int): Key code
            scancode (int): Physical key scan code
            codepoint (str): Unicode character
            modifier (list): Modifier keys

        Returns:
            bool: True if event was handled, else False
        """
        if key == 9:  # Tab key
            if self.ids.inp_username.focus:
                self.ids.inp_passwd.focus = True
                return True
            elif self.ids.inp_passwd.focus:
                self.ids.inp_username.focus = True
                return True
        return False

    def set_focus(self, dt: float) -> None:
        """Set focus to username input field.

        Args:
            dt (float): Time delta since last frame (unused)
        """
        self.ids.inp_username.focus = True

    def _close_popup(self) -> None:
        """Close popup and update application data."""
        if self.app.scr_man.current == "page_setting":
            self.usr_man.change_stat("user_stat", True)
        self.app.load_app_data()
        self.dismiss()
        self.app.start_user_management()
