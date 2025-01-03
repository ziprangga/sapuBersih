import os
import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget


class ResourceManager:

    PATTERNS_GENERAL = [
        # Log files
        "*.log",
        "*.err",
        "*.out",
        # Temporary files
        "*.tmp",
        "*.temp",
        "*~",
        "*.swp",
        "*.tmp~",
        # Cache files
        "*.cache",
        "*.tmp.cache",
        "*.pkg",
    ]

    PATTERN_PREF = ["*.plist"]

    DEFAULT_RECEIPT_PATH = Path("/private/var/db/receipts")
    ADD_RECEIPT_PATH = []

    CACHE_PATH = [
        Path.home() / "Library/Caches",
        Path("/Library/Caches"),
    ]

    TEMP_PATH = [
        Path(os.getenv("TMPDIR", "/private/var/tmp")),
        Path("/private/var/tmp"),
        Path("/tmp"),
        Path("/private/var/folders"),
        Path.home() / "/Library/Saved Application State",
    ]

    APP_LOG_PATH = [
        Path.home() / "Library/Logs",
        Path("/Library/Logs"),
    ]

    APP_SUPPORT_PATH = [
        Path.home() / "Library/Application Support",
        Path("/Library/Application Support"),
    ]

    PREFERENCE_PATH = [
        Path.home() / "Library/Preferences",
        Path("/Library/Preferences"),
    ]

    SCAN_ASSOCIATED = [
        Path.home() / "Library",
        Path.home() / "Library/Application Scripts",
        Path.home() / "Library/Application Support",
        Path.home() / "Library/Application Support/CrashReporter",
        Path.home() / "Library/Containers",
        Path.home() / "Library/Caches",
        Path.home() / "Library/HTTPStorages",
        Path.home() / "Library/Group Containers",
        Path.home() / "Library/Internet Plug-Ins",
        Path.home() / "Library/LaunchAgents",
        Path.home() / "Library/Logs",
        Path.home() / "Library/Preferences",
        Path.home() / "Library/Preferences/ByHost",
        Path.home() / "Library/Saved Application State",
        Path.home() / "Library/WebKit",
        Path("/Library"),
        Path("/Library/Application Support"),
        Path("/Library/Application Support/CrashReporter"),
        Path("/Library/Caches"),
        Path("/Library/Extensions"),
        Path("/Library/Internet Plug-Ins"),
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
        Path("/Library/Logs"),
        Path("/Library/Preferences"),
        Path("/Library/PrivilegedHelperTools"),
        Path("/private/var/db/receipts"),
        Path("/usr/local/bin"),
        Path("/usr/local/etc"),
        Path("/usr/local/opt"),
        Path("/usr/local/sbin"),
        Path("/usr/local/share"),
        Path("/usr/local/var"),
    ]

    APP_PATH = [Path.home() / "Applications", Path("Applications")]

    INCLUDE_APPLE_APP = ["com.apple.", "com.apple.."]

    ICON = "resources/sapuBersih.icns"
    CREDITS = "resources/credits.txt"
    QSS_DARK = "gui/style_dark.qss"
    QSS_LIGHT = "gui/style_light.qss"

    @staticmethod
    def resource_path(relative_path):
        # Dapatkan path absolut ke file sumber daya
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def filter_existing_paths(paths):
        return [path for path in paths if path.exists()]

    @staticmethod
    def get_darwin_user_cache_dir(as_path=False):
        result = subprocess.run(
            ["getconf", "DARWIN_USER_CACHE_DIR"], capture_output=True, text=True
        )
        cache_user_dir = result.stdout.strip()
        return Path(cache_user_dir) if as_path else cache_user_dir

    @staticmethod
    def get_darwin_user_temp_dir(as_path=False):
        result = subprocess.run(
            ["getconf", "DARWIN_USER_TEMP_DIR"], capture_output=True, text=True
        )
        temp_user_dir = result.stdout.strip()
        return Path(temp_user_dir) if as_path else temp_user_dir

    @classmethod
    def receipt_paths(cls, as_string=False):
        paths = [cls.DEFAULT_RECEIPT_PATH] + cls.ADD_RECEIPT_PATH
        return [str(path) for path in paths] if as_string else paths

    @classmethod
    def cache_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.CACHE_PATH]
        return cls.CACHE_PATH

    @classmethod
    def temp_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.TEMP_PATH]
        return cls.TEMP_PATH

    @classmethod
    def log_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.APP_LOG_PATH]
        return cls.APP_LOG_PATH

    @classmethod
    def app_support_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.APP_SUPPORT_PATH]
        return cls.APP_SUPPORT_PATH

    @classmethod
    def preference_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.PREFERENCE_PATH]
        return cls.PREFERENCE_PATH

    @classmethod
    def scan_associated(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.SCAN_ASSOCIATED]
        return cls.SCAN_ASSOCIATED

    @classmethod
    def app_paths(cls, as_string=False):
        if as_string:
            return [str(path) for path in cls.APP_PATH]
        return cls.APP_PATH

    @classmethod
    def gen_patterns(cls):
        return cls.PATTERNS_GENERAL

    @classmethod
    def pref_patterns(cls):
        return cls.PATTERN_PREF

    @classmethod
    def include_apple(cls):
        return cls.INCLUDE_APPLE_APP

    @classmethod
    def icon_path(cls):
        return cls.resource_path(cls.ICON)

    @classmethod
    def credits_path(cls):
        return cls.resource_path(cls.CREDITS)

    @classmethod
    def qss_dark_path(cls):
        return cls.resource_path(cls.QSS_DARK)

    @classmethod
    def qss_light_path(cls):
        return cls.resource_path(cls.QSS_LIGHT)


class StyleManager:
    @staticmethod
    def apply_stylesheet(
        target=None, stylesheet_path_dark=None, stylesheet_path_light=None
    ):
        """Apply stylesheet based on macOS dark mode detection to the target."""
        if not stylesheet_path_dark or not stylesheet_path_light:
            raise ValueError(
                "Both stylesheet_path_dark and stylesheet_path_light must be provided."
            )

        # Detect macOS dark mode
        is_dark_mode = False
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
            )
            is_dark_mode = result.stdout.strip().lower() == "dark"
        except Exception as e:
            print(f"Error detecting dark mode: {e}")

        # Choose the appropriate stylesheet
        stylesheet_path = (
            stylesheet_path_dark if is_dark_mode else stylesheet_path_light
        )

        try:
            with open(stylesheet_path, "r") as file:
                qss = file.read()

            if target is None:
                # Apply globally using QApplication
                QApplication.instance().setStyleSheet(qss)
            elif isinstance(target, QWidget):
                # Apply to a specific QWidget
                target.setStyleSheet(qss)
            else:
                raise ValueError(
                    "Target must be either None, QWidget, or a QMainWindow instance."
                )
        except FileNotFoundError:
            print(f"Stylesheet file not found: {stylesheet_path}")
        except Exception as e:
            print(f"Error applying stylesheet: {e}")
