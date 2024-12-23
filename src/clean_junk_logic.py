import os
import plistlib
from pathlib import Path
from src.utility import ResourceManager as util


class JunkFileCleaner:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    def find_files_by_pattern(self, locations, patterns):
        found_files = set()

        for location in map(Path, locations):
            if not location.exists() or not location.is_dir():
                continue
            self.ui.update_status(f"Searching in {location}...")
            for pattern in patterns:
                found_files.update(map(str, location.rglob(pattern)))
            self.ui.stop_update_status()
        return sorted(found_files)

    def get_uninstalled_apps(self, search_dirs=None):
        try:
            # Default to util.receipt_paths() if search_dirs is None
            if search_dirs is None:
                search_dirs = [
                    Path(path).expanduser() if "~" in path else Path(path)
                    for path in util.receipt_paths() or []
                ]

            uninstalled_apps = set()

            for search_dir in search_dirs:
                # Ensure the directory exists and is valid
                if not search_dir.exists() or not search_dir.is_dir():
                    continue

                try:
                    # Process .bom files in the directory
                    for receipt in search_dir.iterdir():
                        if receipt.is_file() and receipt.suffix == ".bom":
                            uninstalled_apps.add(receipt.stem)
                except (OSError, PermissionError) as e:
                    # Log the error and continue processing other directories
                    print(f"Error accessing {search_dir}: {e}")

            return uninstalled_apps

        except Exception as e:
            # Catch and log unexpected errors
            print(f"Unexpected error: {e}")
            return set()

    def analyze_metadata(self, file_path):
        try:
            with open(file_path, "rb") as plist_file:
                # Load plist data from the file
                plist_data = plistlib.load(plist_file)

            # Attempt to extract the application name or identifier
            return plist_data.get("CFBundleName") or plist_data.get(
                "CFBundleIdentifier"
            )
        except (
            FileNotFoundError,
            plistlib.InvalidFileException,
            KeyError,
            ValueError,
        ) as e:
            # Handle specific exceptions and return None for unsupported files
            return None

    def is_protected_by_sip(self, file_path):
        # sip_paths = util.sip_paths()
        # for protected_path in sip_paths:
        #     if Path(file_path).resolve().as_posix().startswith(str(protected_path)):
        #         return True
        # return False

        sip_paths = [Path(p).resolve() for p in util.sip_paths()]
        resolved_path = Path(file_path).resolve()

        for protected_path in sip_paths:
            # Ensure comparison is based on absolute paths as strings
            if resolved_path.as_posix().startswith(protected_path.as_posix()):
                return True

        return False

    def include_apple_app(self):
        is_checked = self.ui.include_file_checkbox.isChecked()

        if not is_checked:
            apple_apps = util.include_apple()
            if apple_apps:
                return list(apple_apps)

        return []

    def add_file_to_ui(self, files, category):
        for file in files:
            try:
                base_name = os.path.basename(file)
                writable = os.access(file, os.W_OK)
                self.ui.add_tree_item(base_name, file, category, writable)
            except Exception as e:
                print(f"Failed to add file '{file}' to UI: {e}")

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

    def scan_junk_files(self):
        self.ui.clear_tree()

        scan_apple_apps = []
        if self.ui.include_file_checkbox.isChecked():
            if not self.ui.show_question("Are you sure to include Apple applications?"):
                self.ui.include_file_checkbox.setChecked(False)
                return []
            scan_apple_apps = self.include_apple_app()

        try:
            patterns_all = util.patterns_generals()
            patterns_pref = util.patterns_pref()
            uninstalled_apps = self.get_uninstalled_apps()

            temp_files = self.scan_files(
                util.temp_paths(), patterns_all, scan_apple_apps, uninstalled_apps
            )
            cache_files = self.scan_files(
                util.cache_paths(), patterns_all, scan_apple_apps, uninstalled_apps
            )
            pref_files = self.scan_files(
                util.preference_paths(),
                patterns_pref,
                scan_apple_apps,
                uninstalled_apps,
            )
            log_files = self.scan_files(
                util.log_paths(), patterns_all, scan_apple_apps, uninstalled_apps
            )
            app_support_files = self.scan_files(
                util.app_support_paths(),
                patterns_all,
                scan_apple_apps,
                uninstalled_apps,
            )

            # Ensure proper UI association
            self.add_file_to_ui(temp_files, "Temporary Files")
            self.add_file_to_ui(cache_files, "Cache Files")
            self.add_file_to_ui(pref_files, "Preference Files")
            self.add_file_to_ui(log_files, "Log Files")
            self.add_file_to_ui(app_support_files, "Application Support Files")

            return temp_files + cache_files + pref_files + log_files + app_support_files
        except Exception as e:
            print(f"Error during file scanning: {e}")
            return []
