#!/bin/bash

#==============================================================================
# ProxyPal Setup Script
# This script checks for dependencies and installs them.
#==============================================================================

# --- Helper Functions ---
print_success() {
    echo "✅ $1"
}

print_error() {
    echo "❌ Error: $1" >&2
    exit 1
}

print_info() {
    echo "ℹ️  $1"
}

# Use set -e to exit immediately if a command fails
set -e

echo "--- Setting up ProxyPal ---"

# --- 1. Check for and Install Homebrew ---
if ! command -v brew &> /dev/null; then
    print_info "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv)"
    print_success "Homebrew installed."
else
    print_success "Homebrew is already installed."
fi

# --- 2. Check for and Install shadowsocks-libev ---
print_info "Checking for shadowsocks-libev..."
if ! brew list shadowsocks-libev &> /dev/null; then
    print_info "Installing shadowsocks-libev..."
    brew install shadowsocks-libev
    print_success "shadowsocks-libev installed."
else
    print_success "shadowsocks-libev is already installed."
fi

# --- 3. Check for and Install Python Dependencies ---
print_info "Checking for Python 3 and pip..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    print_error "Python 3 and pip3 are required. Please install them."
fi
print_success "Python 3 and pip3 found."

print_info "Installing Python packages (PyQt6, psutil)..."
pip3 install PyQt6 psutil
print_success "Python packages installed."

# --- 4. Set Permissions for the Manager Script ---
print_info "Setting permissions for proxy_manager.sh..."
if [ -f "proxy_manager.sh" ]; then
    chmod +x proxy_manager.sh
    print_success "Permissions set."
else
    print_error "proxy_manager.sh not found in the current directory."
fi

# --- Final Instructions ---
echo
echo "🎉 --- Setup Complete! --- 🎉"
echo
print_info "To run the application, use the following command:"
echo "   ./proxy_manager.sh start"
echo
