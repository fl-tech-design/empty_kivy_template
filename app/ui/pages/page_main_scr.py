# startpage.py
from typing import Any, Dict
from app.services.contr_str import let_up_first
from app.services.logger_config import setup_logger

logger = setup_logger()
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class StartPage(Screen):
    def __init__(self, **kwargs: Dict[str, Any]):
        """
        Initializes the StartPage screen.

        Args:
            app (App): The main application instance.
            **kwargs: Additional keyword arguments passed to the Screen constructor.
        """
        super(StartPage, self).__init__(**kwargs)
        self.app = App.get_running_app()  # Holt die MainApp-Instanz
        self.pop_man = self.app.get_popup_manager()
        self.btn_binds()
        Clock.schedule_once(lambda *args: self.ids.t_box_start.update_theme_colors())

    def upd_page(self, *args):
        """
        Updates the StartPage screen with new text values from the app's base_txt dictionary.

        Args:
            *args: Additional arguments that might be passed when calling this method.
        """
        self.ids.t_box_start.ids.lab_tit_page.text = self.app.base_txt["tit_page_start"]
        self.ids.b_box_startpage.ids.but_1.text = let_up_first(
            self.app.base_txt["settings"]
        )
        self.ids.b_box_startpage.ids.but_2.text = let_up_first(
            self.app.base_txt["exit"]
        )

    def btn_binds(self):
        self.ids.t_box_start.ids.but_info.bind(
            on_release=lambda instance: self.app.get_popup_manager().open_inf_pop(
                "page_start"
            )
        )
