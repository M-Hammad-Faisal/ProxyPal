from setuptools import setup

APP = ["main.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "plist": {
        "LSMinimumSystemVersion": "12.0",
        "NSNetworkUsageDescription": "This app requires network access to connect to a proxy server.",
        "com.apple.security.app-sandbox": True,
        "com.apple.security.network.client": True
    },
    "packages": ["PyQt6"],
    "iconfile": None
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"]
)
