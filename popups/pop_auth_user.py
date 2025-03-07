from kivy.uix.popup import Popup
from kivy.lang import Builder
from constants import DIR_POPS
from contr_str import let_uppercase_first
from libs.user_management import UserManager
from popups.pop_info import Pop_Info

Builder.load_file(DIR_POPS + "pop_auth_user.kv")


class Pop_Auth_User(Popup):
    def __init__(self, app, mode, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.mode = mode
        self.user_manager = UserManager()
        self._update_labels()

    def _update_labels(self):
        if self.mode == "register":
            self.title = self.app.base_txt["create_user"]
            self.ids.lab_inf_create_user.text = self.app.base_txt["inf_create_user"]
        else:
            self.title = self.app.base_txt["login_user"]
            self.ids.lab_inf_create_user.text = self.app.base_txt["inf_login_user"]
        
        self.ids.inp_username.hint_text = let_uppercase_first(
            self.app.base_txt["username"]
        )
        self.ids.inp_passwd.hint_text = let_uppercase_first(
            self.app.base_txt["password"]
        )

        self.ids.but_confirm.text = let_uppercase_first(self.app.base_txt["confirm"])
        self.ids.but_chancel.text = let_uppercase_first(self.app.base_txt["chancel"])

    def but_confirm_released(self):
        """
        Verarbeitet die Erstellung eines neuen Benutzers.
        """
        username = self.ids.inp_username.text.strip()
        password = self.ids.inp_passwd.text.strip()

        if not username:
            self.ids.inp_username.hint_text = let_uppercase_first(
                self.app.base_txt["please_enter_a_username"]
            )
            return

        if not password:
            self.ids.inp_passwd.hint_text = let_uppercase_first(
                self.app.base_txt["please_enter_a_pw"]
            )
            return

        try:
            if self.mode == 'login':
                if self.user_manager.verify_password(username, password):
                    self.user_manager.change_login_state(True)
                    self._close_popup()
                else:
                    popup_err_login = Pop_Info(self.app, self.app.base_txt["inf_err_login"])
                    popup_err_login.open()
                    
            elif self.mode == 'register':
                hashed_pw = self.user_manager.hash_password(password)
                self.user_manager.add_new_user_to_list(username, hashed_pw)
                self.user_manager.change_user_stat(True)
                self.user_manager.change_login_state(True)
                self._close_popup()
                
        except Exception as e:
            popup_err_login = Pop_Info(self.app, str(e))
            popup_err_login.open()


    def _close_popup(self):
        self.app.load_app_data()
        self.dismiss()
        self.app.start_user_management()
