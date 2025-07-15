# **ProxyPal**

ProxyPal is a modern, user-friendly desktop client for managing Shadowsocks connections on **macOS**. Inspired by the
clean interface of Outline, it provides a simple and elegant way to manage and switch between multiple proxy servers.

The application is built with **Python** and **PyQt6** and is designed to integrate seamlessly into the macOS
environment with features like a menu bar icon and automatic theme switching.

---

## 🤔 Why ProxyPal?

This project was born out of a real-world need. Like many others, I was having issues getting the official Outline
client to work consistently on my Mac. After a fresh installation, it simply wouldn't open. I soon discovered that
several of my friends were facing the exact same problem on their machines.

I decided to create a solution. Since my background is in Python, not Swift or other native macOS languages, I built a
new Shadowsocks client from the ground up using the tools I knew best: Python and the powerful PyQt6 framework.

What started as a personal fix has grown into a fully-featured application. ProxyPal is the result of that effort—a
reliable, modern, and easy-to-use client for anyone who needs a stable way to manage their proxy connections on a Mac. I
hope it helps you as much as it has helped me and my friends!

---

## ✨ Features

- **Multi-Server Management**: Add, save, and manage a list of multiple Shadowsocks servers.
- **System Tray Integration**: Lives in the macOS menu bar for quick access to connection status and the main window.
- **Automatic Proxy Configuration**: Uses a companion bash script (`proxy_manager.sh`) to automatically configure
  system-wide
  proxy settings with `sudo`, so you don't have to do it manually.
- **Dynamic Light & Dark Mode**: Automatically adapts its appearance to match your macOS system theme in real-time.
- **Smart Clipboard Detection**: Automatically detects and offers to pre-fill the "Add Server" dialog when a valid ss://
  access key is copied to the clipboard.
- **Polished User Experience**: Includes a friendly onboarding screen for new users and a clean, intuitive interface for
  managing connections.
- **Functional Feedback System**: Allows users to send feedback directly to the developer via a web form.
- **Modern UI**: Aesthetically pleasing interface built with Python and PyQt6, inspired by the Outline client.

---

## 📋 Requirements

Before you begin, ensure you have the following installed on your macOS system:

- **Python 3**: The application is written in Python 3.
- **pip**: The Python package installer.
- **Homebrew**: The package manager for macOS, used to install `shadowsocks-libev`.

The `setup.sh` script will handle installing the necessary Python packages and `shadowsocks-libev`.

---

## 🚀 Getting Started

Follow these steps to get ProxyPal up and running.

**1. Clone the Repository**
Clone or download the project files to your local machine.

```Bash
git clone https://github.com/M-Hammad-Faisal/proxypal.git
cd proxypal
```

**2. Run the Setup Script**
The `setup.sh` script will check for dependencies and install everything you need. You only need to run this once.

```Bash
chmod +x setup.sh
./setup.sh
```

**3. Make the Manager Script Executable**
The `proxy_manager.sh` script requires execute permissions to run. You only need to do this once.

```Bash
chmod +x proxy_manager.sh
```

**3. Run the Application**
The **only** command you need to run the application is:

```Bash
./proxy_manager.sh start
```

This script will:

- Prompt for your **sudo** password to gain permission to change system network settings.
- Launch the ProxyPal GUI application.
- Automatically handle enabling and disabling the system proxy when you connect or disconnect.

---

## 📖 How to Use

- **Adding a Server:**
    - Copy a `ss://` access key to your clipboard.
    - Go to **File > Add Server** in the menu bar. The key will be automatically pasted for you.
    - Click "Confirm" to add the server to your list.

- **Connecting/Disconnecting:**
    - Click the "CONNECT" button on any server card to establish a connection.
    - ProxyPal will automatically disconnect any previously active server.
    - Click "DISCONNECT" on the active server to terminate the connection.

- **Managing Servers:**
    - Click the three-dot menu on any server card to **Rename** or **Forget** (delete) it.

- **Using the Tray Icon:**
    - The app lives in your macOS menu bar.
    - **Right-click** (or control-click) the icon to open a menu where you can see the connection status, open the
      window, or quit the application.

---

## 📂 Project Structure

The project is organized into two main directories:

- `core/`: Contains the backend logic for the application.
    - `connection.py`: Manages the `ss-local` subprocess and connection lifecycle.
    - `parser.py`: Handles parsing of `ss://` access keys.
    - `storage.py`: Manages saving and loading server configurations.
- `ui/`: Contains all the user interface components.
    - `main_window.py`: The main application window and central controller.
    - `server_widget.py`: The UI for a single server card.
    - `onboarding_widget.py`: The welcome screen for new users.
    - `dialogs.py`: Custom dialog boxes for adding servers and submitting feedback.
    - `icons.py`: A helper module to create and manage all application icons from SVG paths.
    - `styles.py` & `theme.py`: Manages the application's visual appearance and dynamic themes.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or find a bug, please feel free to open an issue or submit
a pull request.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.