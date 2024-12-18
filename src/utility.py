import os
import sys
from pathlib import Path


# Konstanta global
DEFAULT_RECEIPT_PATH = Path("/private/var/db/receipts")
ADD_RECEIPT_PATH = []


CACHE_PATH = [
    Path.home() / "Library/Caches",
    Path("/Library/Caches"),
]

PREFERENCE_PATH = [
    Path.home() / "Library/Preferences",
    Path("/Library/Preferences"),
]

TEMP_PATH = [
    Path(os.getenv("TMPDIR", "/private/var/tmp")),
    Path("/private/var/tmp"),
    Path("/tmp"),
    Path("/private/var/folders"),
    Path("/Library/Caches"),
    Path.home() / "Library/Caches",
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


# Fungsi
def resource_path(relative_path):
    """Dapatkan path absolut ke file sumber daya."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def receipt_paths(as_string=False):
    paths = [DEFAULT_RECEIPT_PATH] + ADD_RECEIPT_PATH
    return [str(path) for path in paths] if as_string else paths


def cache_paths(as_string=False):
    if as_string:
        return [str(path) for path in CACHE_PATH]
    return CACHE_PATH


def preference_paths(as_string=False):
    if as_string:
        return [str(path) for path in PREFERENCE_PATH]
    return PREFERENCE_PATH


def temp_paths(as_string=False):
    if as_string:
        return [str(path) for path in TEMP_PATH]
    return TEMP_PATH


def scan_associated(as_string=False):
    if as_string:
        return [str(path) for path in SCAN_ASSOCIATED]
    return SCAN_ASSOCIATED
