# pop_auth_user.py
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

from constants import DIR_POPS, USER_MANAGEMENT
from app.services.contr_str import let_up_first
from app.ui.popups.pop_info import Pop_Info

Builder.load_file(DIR_POPS + "pop_auth_user.kv")


class Pop_Auth_User(Popup):
    def __init__(self, mode, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.mode = mode
        if USER_MANAGEMENT:
            self.user_manager = self.app.get_user_manager()
        Clock.schedule_once(self.set_focus)
        Window.bind(on_key_down=self.on_key_down)

        self._update_labels()

    def _update_labels(self):
        if self.mode == "register":
            self.title = self.app.base_txt["create_user"]
            self.ids.lab_inf_create_user.text = self.app.base_txt["inf_create_user"]
        else:
            self.title = self.app.base_txt["login_user"]
            self.ids.lab_inf_create_user.text = self.app.base_txt["inf_login_user"]

        self.ids.inp_username.hint_text = let_up_first(
            self.app.base_txt["username"]
        )
        self.ids.inp_passwd.hint_text = let_up_first(
            self.app.base_txt["password"]
        )

        self.ids.but_confirm.text = let_up_first(self.app.base_txt["confirm"])
        self.ids.but_chancel.text = let_up_first(self.app.base_txt["chancel"])

    def but_confirm_released(self):
        """
        Verarbeitet die Erstellung eines neuen Benutzers.
        """
        username = self.ids.inp_username.text.strip()
        password = self.ids.inp_passwd.text.strip()

        if not username:
            self.ids.inp_username.hint_text = let_up_first(
                self.app.base_txt["please_enter_a_username"]
            )
            return

        if not password:
            self.ids.inp_passwd.hint_text = let_up_first(
                self.app.base_txt["please_enter_a_pw"]
            )
            return

        try:
            if self.mode == "login":
                if self.user_manager.verify_password(username, password):
                    self.user_manager.change_stat("login_stat", True)
                    self._close_popup()
                else:
                    popup_err_login = Pop_Info(
                        self.app, self.app.base_txt["inf_err_login"]
                    )
                    popup_err_login.open()

            elif self.mode == "register":
                hashed_pw = self.user_manager.hash_password(password)
                self.user_manager.add_new_user_to_list(username, hashed_pw)
                self.user_manager.change_stat("user_stat",True)
                self.user_manager.change_stat("login_stat",True)
                self._close_popup()

        except Exception as e:
            popup_err_login = Pop_Info(self.app, str(e))
            popup_err_login.open()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """Tab-Taste abfangen und Fokus wechseln"""
        if key == 9:  # Tab-Taste
            if self.ids.inp_username.focus:
                self.ids.inp_passwd.focus = True
                return True  # Standard-Tab-Verhalten unterdrücken
            elif self.ids.inp_passwd.focus:
                self.ids.inp_username.focus = True
                return True
        return False

    def set_focus(self, dt):
        self.ids.inp_username.focus = True

    def _close_popup(self):
        self.app.load_app_data()
        self.dismiss()
        self.app.start_user_management()
