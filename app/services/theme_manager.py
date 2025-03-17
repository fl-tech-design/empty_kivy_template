# theme_manager.py
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty


class ThemeManager(EventDispatcher):
    themes = DictProperty({})
    current_theme = StringProperty("dark")  # Muss als Property deklariert werden!

    def __init__(self):
        super().__init__()
        self.app = App.get_running_app()
        self.themes = self.app.base_data.get("themes", {})
        self.current_theme = "dark"  # Muss explizit gesetzt werden

    def change_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            Clock.schedule_once(lambda dt: self.app.setting_page.children[0].upd_page(), 0)
        else:
            raise ValueError(f"Theme '{theme_name}' existiert nicht!")
