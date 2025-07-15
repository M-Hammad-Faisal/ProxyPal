import json
import time
from pathlib import Path

APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / "ProxyPal"

CONFIG_FILE = APP_SUPPORT_DIR / "servers.json"
FEEDBACK_FILE = APP_SUPPORT_DIR / "feedback.json"


def _ensure_dir_exists():
    """
    A helper function to ensure the application support directory exists.
    It creates the directory if it's not already there.
    """
    APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_servers() -> list:
    """
    Loads all server configurations from the standard application support directory.

    Returns:
        A list of server configuration dictionaries, or an empty list if not found.
    """
    _ensure_dir_exists()
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_servers(server_configs: list):
    """
    Saves the entire list of server configurations to the application support directory.

    Args:
        server_configs: The full list of server configuration dictionaries.
    """
    _ensure_dir_exists()
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(server_configs, f, indent=4)
    except IOError as e:
        print(f"Error saving server configurations: {e}")


def add_server(new_config: dict):
    """
    Adds a new server configuration to the list and saves it.
    Prevents adding a server if one with the same ID already exists.
    """
    servers = load_servers()
    if any(s['id'] == new_config['id'] for s in servers):
        print(f"Server with ID {new_config['id']} already exists. Not adding.")
        return
    servers.append(new_config)
    save_servers(servers)


def delete_server(server_id: str):
    """
    Deletes a server configuration from the list by its ID and saves the change.
    """
    servers = load_servers()
    servers_to_keep = [s for s in servers if s.get('id') != server_id]
    save_servers(servers_to_keep)


def save_feedback(feedback_message: str):
    """
    Saves a user's feedback message to a JSON file with a timestamp.
    """
    _ensure_dir_exists()
    feedback_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": feedback_message
    }

    try:
        feedbacks = []
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, "r") as f:
                try:
                    feedbacks = json.load(f)
                except json.JSONDecodeError:
                    feedbacks = []

        feedbacks.append(feedback_entry)

        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedbacks, f, indent=4)

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving feedback: {e}")
