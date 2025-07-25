#!/bin/bash

#==============================================================================
# ProxyPal Setup Script (with Virtual Environment)
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

# --- 3. Create Python Virtual Environment ---
print_info "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required. Please install it."
fi
print_success "Python 3 found."

print_info "Creating Python virtual environment in './venv'..."
python3 -m venv venv
print_success "Virtual environment created."

# --- 4. Install Python Dependencies into Virtual Environment ---
print_info "Installing Python packages from requirements.txt..."
# Use the pip from the newly created venv to install packages
./venv/bin/pip install -r requirements.txt
print_success "Python packages installed."

# --- 5. Set Permissions for the Manager Script ---
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
