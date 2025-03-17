# data_manager.py
import json
from typing import Dict, Any
from constants import BASE_DATA
from app.services.logger_config import setup_logger

logger = setup_logger()

def save_base_data(data: Dict[str, Any]) -> None:
    """
    Speichert Daten in eine JSON-Datei.

    :param file_path: Der Pfad zur JSON-Datei
    :param data: Die Daten, die in der JSON-Datei gespeichert werden sollen
    """
    try:
        with open(BASE_DATA, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logger.error(f"Error saving JSON file {BASE_DATA}: {e}")


def update_base_data(key: str, new_value: Any) -> None:
    """
    Ändert den Wert eines bestimmten Schlüssels in einer JSON-Datei.

    :param key: Der Schlüssel des Wertes, der geändert werden soll
    :param new_value: Der neue Wert, der dem Schlüssel zugewiesen werden soll
    """
    data = read_from_json(BASE_DATA)

    if key in data:
        data[key] = new_value
        save_base_data(data)
    else:
        logger.error(f"Schlüssel '{key}' nicht gefunden.")


def read_from_json(f_path: str) -> Dict[str, Any]:
    """
    Lädt eine JSON-Datei und gibt ihren Inhalt zurück.
    :return: Der Inhalt der JSON-Datei oder ein leeres Dictionary im Fehlerfall
    """
    try:
        with open(f_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading JSON file {f_path}: {e}")
        return {}


def save_to_json(f_path: str, data: Dict[str, Any]) -> None:
    """
    Speichert Daten in eine JSON-Datei.

    :param file_path: Der Pfad zur JSON-Datei
    :param data: Die Daten, die in der JSON-Datei gespeichert werden sollen
    """
    try:
        with open(f_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logger.error(f"Error saving JSON file {f_path}: {e}")

