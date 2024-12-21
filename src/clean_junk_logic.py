import os
import plistlib
from pathlib import Path
from src.utility import ResourceManager as util


class JunkFileCleaner:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    # Base Script
    def find_files_by_pattern(self, locations, patterns):
        # Temukan file berdasarkan pola dalam lokasi tertentu
        found_files = set()
        for location in locations:
            location_path = Path(location)
            self.ui.update_status(f"Searching in {location_path}...")
            if location_path.exists() and location_path.is_dir():
                for pattern in patterns:
                    found_files.update(
                        str(match) for match in location_path.rglob(pattern)
                    )
            self.ui.stop_update_status()
        return list(found_files)

    # addon
    def get_uninstalled_apps(self, search_dirs=None):
        if search_dirs is None:
            search_dirs = [Path(path).expanduser() for path in util.receipt_paths()]
        uninstalled_apps = set()

        for search_dir in search_dirs:
            if search_dir.exists() and search_dir.is_dir():
                for receipt in search_dir.iterdir():
                    if receipt.is_file() and receipt.suffix == ".bom":
                        app_name = receipt.stem
                        uninstalled_apps.add(app_name)
        return uninstalled_apps

    # addon
    def analyze_metadata(self, file_path):
        try:
            with open(file_path, "rb") as plist_file:
                plist_data = plistlib.load(plist_file)
                # Extract metadata, such as the application name
                app_name = plist_data.get("CFBundleName", None) or plist_data.get(
                    "CFBundleIdentifier", None
                )
                return app_name
        except Exception as e:
            return None

    # addon
    def is_protected_by_sip(self, file_path):
        for protected_path in util.sip_paths():
            if Path(file_path).resolve().as_posix().startswith(str(protected_path)):
                return True
        return False

    # Base Script
    def include_apple_app(self):
        status = self.ui.include_file_checkbox.isChecked()

        paths = set()

        if status:
            paths.update()
        else:
            include_apps = util.include_apple()
            if include_apps:
                paths.update(include_apps)
        return list(paths)

    # Base Script modified
    def scan_files(self, scan_path, patterns, included_apps, uninstalled_apps):
        found_files = []
        all_files = self.find_files_by_pattern(scan_path, patterns)
        for file in all_files:
            # Exclude SIP-protected files
            if self.is_protected_by_sip(file):
                continue
            # Skip included apps (still installed and should not be removed)
            if any(included in file for included in included_apps):
                continue
            # Include files related to uninstalled apps
            app_name = self.analyze_metadata(file)
            if app_name and app_name in uninstalled_apps:
                found_files.append(file)
                continue
            # Include files not belonging to any app (generic junk)
            found_files.append(file)
        return found_files

    def add_file_to_ui(self, files, category):
        for file in files:
            base_name = os.path.basename(file)
            writable = os.access(file, os.W_OK)
            self.ui.add_tree_item(base_name, file, category, writable)

    # Base Script modified
    def scan_junk_files(self):
        self.ui.clear_tree()

        patterns_all = util.patterns_generals()
        patterns_pref = util.patterns_pref()

        if self.ui.include_file_checkbox.isChecked():
            confirm = self.ui.show_question(
                "Are you sure to include Apple applications?"
            )
            if confirm:
                scan_apple_apps = self.include_apple_app()
            else:
                self.ui.include_file_checkbox.setChecked(False)
                scan_apple_apps = []
                return []
        else:
            scan_apple_apps = self.include_apple_app()

        uninstalled_apps = self.get_uninstalled_apps()

        # send to scan
        app_support_files = self.scan_files(
            util.app_support_paths(),
            patterns_all,
            scan_apple_apps,
            uninstalled_apps,
        )
        log_files = self.scan_files(
            util.log_paths(), patterns_all, scan_apple_apps, uninstalled_apps
        )
        temp_files = self.scan_files(
            util.temp_paths(), patterns_all, scan_apple_apps, uninstalled_apps
        )
        cache_files = self.scan_files(
            util.cache_paths(), patterns_all, scan_apple_apps, uninstalled_apps
        )
        pref_files = self.scan_files(
            util.preference_paths(), patterns_pref, scan_apple_apps, uninstalled_apps
        )

        # add to ui
        self.add_file_to_ui(temp_files, "Temporary Files")
        self.add_file_to_ui(cache_files, "Cache Files")
        self.add_file_to_ui(pref_files, "Preference Files")
        self.add_file_to_ui(log_files, "Log Files")
        self.add_file_to_ui(app_support_files, "Application Support Files")

        return temp_files + cache_files + pref_files + log_files + app_support_files
