import subprocess
import sys

NETWORK_SERVICE = "Wi-Fi"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = "1080"


def set_proxy(enable=True):
    """Enables or disables the system SOCKS proxy using direct shell commands."""
    state = "on" if enable else "off"
    print(f"🔄 Turning system proxy {state} for '{NETWORK_SERVICE}'...")

    try:
        if enable:
            set_command = f"/usr/sbin/networksetup -setsocksfirewallproxy '{NETWORK_SERVICE}' {PROXY_HOST} {PROXY_PORT}"
            subprocess.run(set_command, check=True, shell=True, capture_output=True, text=True)

        state_command = f"/usr/sbin/networksetup -setsocksfirewallproxystate '{NETWORK_SERVICE}' {state}"
        subprocess.run(state_command, check=True, shell=True, capture_output=True, text=True)

        status = "✅ Connected" if enable else "🔌 Disconnected"
        print(status)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: Failed to execute command.")
        print(f"   Details: {e.stderr.strip()}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        print("--- Proxy Controller ---")
        print("Make sure your local proxy is running.")

        set_proxy(enable=True)

        input("\nPress Enter to disconnect and exit...\n")

    finally:
        set_proxy(enable=False)
