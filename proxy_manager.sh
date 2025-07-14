#!/bin/bash

#==============================================================================
# Proxy Manager: A script to control the system SOCKS proxy and launch a GUI.
#==============================================================================

# --- Configuration ---
readonly NETWORK_SERVICE="Wi-Fi"
readonly PROXY_HOST="127.0.0.1"
readonly PROXY_PORT="1080"
readonly PYTHON_APP_COMMAND="python3 main.py"

# --- Functions ---
start_proxy() {
    echo "🔄 Enabling system proxy for '$NETWORK_SERVICE'..."
    sudo networksetup -setsocksfirewallproxy "$NETWORK_SERVICE" "$PROXY_HOST" "$PROXY_PORT"
    sudo networksetup -setsocksfirewallproxystate "$NETWORK_SERVICE" on
    if [ $? -eq 0 ]; then
        echo "✅ Proxy CONNECTED."
    else
        echo "❌ Error: Failed to enable the proxy." >&2; exit 1
    fi
}

stop_proxy() {
    echo "🔄 Disabling system proxy for '$NETWORK_SERVICE'..."
    sudo networksetup -setsocksfirewallproxystate "$NETWORK_SERVICE" off
    echo "🔌 Proxy DISCONNECTED."
}

# --- Main Logic ---
trap stop_proxy EXIT

case "$1" in
    start)
        start_proxy
        echo "🚀 Launching Python GUI..."
        exec $PYTHON_APP_COMMAND
        ;;
    *)
        echo "Usage: $0 start"; exit 1
        ;;
esac