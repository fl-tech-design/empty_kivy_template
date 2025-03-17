"""
This module defines the Page_Start screen, which serves as the main starting page of the application.
It includes functionality for updating the UI with dynamic text and binding button actions.
"""

from constants import PATH_TO_MAINLOGO_D, PATH_TO_MAINLOGO_L

from typing import Any, Dict
from app.services.contr_str import let_up_first

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class Page_Start(Screen):
    def __init__(self, **kwargs: Dict[str, Any]):
        """
        Initializes the Page_Start screen.

        Args:
            **kwargs: Additional keyword arguments passed to the Screen constructor.
        """
        super(Page_Start, self).__init__(**kwargs)
        self.app = App.get_running_app()  # Retrieve the main application instance
        self.pop_man = self.app.get_pop_man()
        self.btn_binds()
        Clock.schedule_once(lambda *args: self.ids.t_box_start.update_theme_colors())

    def upd_page(self, *args: Any) -> None:
        """
        Updates the Page_Start screen with new text values from the app's base_txt dictionary.

        This method dynamically updates the labels, buttons, and images on the screen based on the
        current language or theme settings stored in the app's base_txt dictionary.

        Args:
            *args: Additional arguments that might be passed when calling this method.
        """
        self.set_img_sources()
        self.ids.t_box_start.ids.lab_tit_page.text = self.app.base_txt["tit_page_start"]
        self.ids.b_box_startpage.ids.but_1.text = let_up_first(
            self.app.base_txt["settings"]
        )
        self.ids.b_box_startpage.ids.but_2.text = let_up_first(
            self.app.base_txt["exit"]
        )

    def btn_binds(self) -> None:
        """
        Binds button actions to their respective event handlers.

        This method ensures that buttons on the Page_Start screen are connected to
        their corresponding popup or action logic.
        """
        self.ids.t_box_start.ids.but_info.bind(
            on_release=lambda instance: self.app.get_popup_manager().open_inf_pop(
                "page_start"
            )
        )

    def set_img_sources(self) -> None:
        """
        Sets the image sources for the logo based on the current theme.

        If the current theme is "dark", the dark version of the logo is used.
        Otherwise, the light version of the logo is used.
        """
        if self.app.theme_manager.current_theme == "dark":
            self.ids.t_box_start.ids.img_logo_main.source = PATH_TO_MAINLOGO_D
        else:
            self.ids.t_box_start.ids.img_logo_main.source = PATH_TO_MAINLOGO_L
