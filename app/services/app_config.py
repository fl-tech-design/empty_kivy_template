## configuration of kivy
from constants import CONFIG_STAT
from kivy.config import Config


def start_app_config():
    if CONFIG_STAT:
        config_win_size()


def config_win_size(h: str = "850", w: str = "850") -> None:
    """
    Configure Kivy window dimensions and resizable state.

    Sets the initial window size and enables/disables resizing capability.
    Must be called BEFORE creating the App instance to take effect.
    Configuration is persisted to the Kivy config file.

    Args:
        h (str): Window height in pixels (default: "850")
        w (str): Window width in pixels (default: "850")

    Example:
        config_win_size("1080", "1920")  # Sets 1920x1080 window
    """
    Config.set("graphics", "resizable", "1")
    Config.set("graphics", "height", h)
    Config.set("graphics", "width", w)
    Config.write()
