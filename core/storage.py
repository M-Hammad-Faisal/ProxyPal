import json
from pathlib import Path

APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / "ProxyPal"

CONFIG_FILE = APP_SUPPORT_DIR / "servers.json"


def _ensure_dir_exists():
    """Ensures the application support directory exists."""
    APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_servers() -> list:
    """Loads all server configurations from the standard application support directory."""
    _ensure_dir_exists()
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_servers(server_configs: list):
    """Saves the entire list of server configurations to the application support directory."""
    _ensure_dir_exists()
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(server_configs, f, indent=4)
    except IOError as e:
        print(f"Error saving server configurations: {e}")


def add_server(new_config: dict):
    """Adds a new server configuration to the list and saves it."""
    servers = load_servers()
    if any(s['id'] == new_config['id'] for s in servers):
        print(f"Server with ID {new_config['id']} already exists. Not adding.")
        return
    servers.append(new_config)
    save_servers(servers)


def delete_server(server_id: str):
    """Deletes a server configuration from the list by its ID."""
    servers = load_servers()
    servers_to_keep = [s for s in servers if s.get('id') != server_id]
    save_servers(servers_to_keep)
