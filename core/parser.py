import base64
import binascii
from urllib.parse import urlparse, parse_qs, unquote


def parse_access_key(key: str) -> dict:
    """
    Parses a Shadowsocks (ss://) access key into a configuration dictionary.
    Handles standard and Outline-generated keys.

    Args:
        key: The ss:// access key string.

    Returns:
        A dictionary containing the server configuration.

    Raises:
        ValueError: If the key format is invalid.
    """
    if not key.startswith("ss://"):
        raise ValueError("Key must start with ss://")

    try:
        parsed_url = urlparse(key)

        if '@' not in parsed_url.netloc:
            raise ValueError("Invalid key format: missing '@' separator.")

        encoded_user_info, server_address = parsed_url.netloc.rsplit('@', 1)

        if ':' not in server_address:
            raise ValueError("Invalid server format: must be server:port.")

        server, port_str = server_address.split(':', 1)
        port = int(port_str)

        padding_needed = -len(encoded_user_info) % 4
        if padding_needed:
            encoded_user_info += '=' * padding_needed

        decoded_user_info = base64.urlsafe_b64decode(encoded_user_info).decode('utf-8')
        method, password = decoded_user_info.split(':', 1)

    except (ValueError, binascii.Error, UnicodeDecodeError, TypeError) as e:
        raise ValueError(f"Could not parse the access key. Details: {e}")

    config = {
        "id": key,
        "server": server,
        "server_port": port,
        "password": password,
        "method": method,
        "name": server
    }

    query_params = parse_qs(parsed_url.query)
    if 'outline' in query_params:
        config['name'] = f"Outline Server ({server})"
    elif 'name' in query_params:
        config['name'] = unquote(query_params['name'][0])

    return config
