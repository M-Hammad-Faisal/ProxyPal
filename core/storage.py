import json
import os
import time

CONFIG_FILE = "proxypal_servers.json"
FEEDBACK_FILE = "proxypal_feedback.json"


def load_servers() -> list:
    """
    Loads all server configurations from the local JSON file.

    Returns:
        A list of server configuration dictionaries, or an empty list if not found.
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_servers(server_configs: list):
    """
    Saves the entire list of server configurations to the JSON file.

    Args:
        server_configs: The full list of server configuration dictionaries.
    """
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
    feedback = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": feedback_message
    }
    try:
        feedbacks = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r") as f:
                feedbacks = json.load(f)

        feedbacks.append(feedback)

        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedbacks, f, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving feedback: {e}")
