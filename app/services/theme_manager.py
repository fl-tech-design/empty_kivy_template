# theme_manager.py
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty


class ThemeManager(EventDispatcher):
    themes = DictProperty({})
    current_theme = StringProperty("dark")  # Muss als Property deklariert werden!

    def __init__(self):
        super().__init__()
        app = App.get_running_app()
        self.themes = app.base_data.get("themes", {})
        self.current_theme = "dark"  # Muss explizit gesetzt werden

    def change_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' existiert nicht!")
