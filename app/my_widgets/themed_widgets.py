# themed_widgets.py
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.app import App
from kivy.clock import Clock  # Neu hinzugefügt


class Lbl_Big(Label):
    color_key = StringProperty("text_color")  # Neu hinzugefügt

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Verzögerte Initialisierung
        Clock.schedule_once(self._setup_theme, 0)  # Neu hinzugefügt

    def _setup_theme(self, *args):
        """Sichere Initialisierung des Themes"""
        app = App.get_running_app()
        if app and hasattr(app, "theme_manager"):
            self.theme_manager = app.theme_manager
            self.theme_manager.bind(current_theme=self.update_color)
            self.update_color()

    def update_color(self, *args):
        """Aktualisiert die Farbe basierend auf dem aktuellen Theme"""
        theme_colors = self.theme_manager.themes.get(  # self.theme_manager verwenden
            self.theme_manager.current_theme, {}
        )
        self.color = theme_colors.get(self.color_key, [0, 0, 0, 1])


# Gleiche Anpassungen für Lbl_Small und Btn_Clear


class Lbl_Small(Label):
    color_key = StringProperty("text_color")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._setup_theme, 0)  # Neu hinzugefügt

    def _setup_theme(self, *args):
        app = App.get_running_app()
        if app and hasattr(app, "theme_manager"):
            self.theme_manager = app.theme_manager
            self.theme_manager.bind(current_theme=self.update_color)
            self.update_color()

    def update_color(self, *args):
        theme_colors = self.theme_manager.themes.get(
            self.theme_manager.current_theme, {}
        )
        self.color = theme_colors.get(self.color_key, [0, 0, 0, 1])


class Btn_Clear(Button):
    color_key = StringProperty("text_color")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._setup_theme, 0)  # Neu hinzugefügt

    def _setup_theme(self, *args):
        app = App.get_running_app()
        if app and hasattr(app, "theme_manager"):
            self.theme_manager = app.theme_manager
            self.theme_manager.bind(current_theme=self.update_color)
            self.update_color()

    def update_color(self, *args):
        theme_colors = self.theme_manager.themes.get(
            self.theme_manager.current_theme, {}
        )
        self.color = theme_colors.get(self.color_key, [0, 0, 0, 1])
