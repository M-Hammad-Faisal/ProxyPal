import json
import time
import os

CONFIG_FILE = "proxypal_servers.json"
FEEDBACK_FILE = "proxypal_feedback.json"


def save_servers(server_configs: list):
    """
    Saves a list of server configurations to a local JSON file.

    Args:
        server_configs: A list of server configuration dictionaries.
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(server_configs, f, indent=4)
    except IOError as e:
        print(f"Error saving server configurations: {e}")


def load_servers() -> list:
    """
    Loads server configurations from the local JSON file.

    Returns:
        A list of server configuration dictionaries, or an empty list if not found.
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No saved servers found or configuration file is invalid.")
        return []


def save_feedback(feedback_message: str):
    """
    Saves a user's feedback message to a JSON file with a timestamp.

    Args:
        feedback_message: The feedback string from the user.
    """
    feedback = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": feedback_message
    }
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r") as f:
                feedbacks = json.load(f)
        else:
            feedbacks = []

        feedbacks.append(feedback)

        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedbacks, f, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving feedback: {e}")
