import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Konfiguriert und gibt einen standardisierten Logger zurück"""
    logger = logging.getLogger("my_app_logger")
    logger.setLevel(logging.DEBUG)

    # Erstelle File Handler mit Rotation
    handler = RotatingFileHandler("app.log", maxBytes=1048576, backupCount=5)
    handler.setLevel(logging.DEBUG)

    # Formatierung
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Handler zum Logger hinzufügen
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
