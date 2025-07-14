import socket


def find_available_port(start_port: int) -> int:
    """
    Finds an available TCP port on localhost, starting from a given port.

    Args:
        start_port: The port number to start searching from.

    Returns:
        An available port number.

    Raises:
        IOError: If no free ports are found.
    """
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
    raise IOError("No free ports found on localhost.")

