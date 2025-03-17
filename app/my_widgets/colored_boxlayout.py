# colored_boxlayout.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle


class ColoredBoxLayoutBase(BoxLayout):
    background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._setup_theme, 0)  # Verzögerter Setup

    def _setup_theme(self, *args):
        """Sichere Initialisierung des Themes"""
        app = App.get_running_app()
        if not app or not hasattr(app, "theme_manager"):
            Clock.schedule_once(
                self._setup_theme, 0.1
            )  # Wiederhole, falls App noch nicht bereit
            return
        self.theme_manager = app.theme_manager
        self.theme_manager.bind(current_theme=self.update_theme_colors)
        self.update_theme_colors()  # Initialer Farb-Update

    def update_theme_colors(self, *args):
        """Aktualisiert die Hintergrundfarbe basierend auf dem aktuellen Theme"""
        # Sichere Farb-Abfrage
        theme = self.theme_manager.current_theme if self.theme_manager else "light"
        theme_colors = self.theme_manager.themes.get(theme, {})

        # Fallback für ungültige Farben
        default_color = [1, 1, 1, 1]
        self.background_color = theme_colors.get(self.color_key, default_color)
        # Sicherheit für 4-Element-Farben
        if len(self.background_color) != 4:
            self.background_color = default_color

        self.update_background()

    def update_background(self, *args):
        """Aktualisiert das Canvas sicher"""
        with self.canvas.before:
            self.canvas.before.clear()  # Nur das before-Canvas leeren
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)

        # Bindungen für Position/Größe
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *args):
        """Wird aufgerufen, wenn Position/Größe ändern"""
        self.update_background()


# Spezifische BoxLayout-Klassen
class ColBoxLayout_1(ColoredBoxLayoutBase):
    """boxlayout for background 1"""

    pass


class ColBoxLayout_2(ColoredBoxLayoutBase):
    """boxlayout for backgound 2"""

    pass


class ColBoxLayout_3(ColoredBoxLayoutBase):
    """boxlayout for backgound 3"""

    pass


class ColBoxLayout_4(ColoredBoxLayoutBase):
    """boxlayout for foreground 1 to make lines"""

    pass


class ColBoxLayout_4(ColoredBoxLayoutBase):
    """boxlayout for foreground 2 to make lines"""

    pass
