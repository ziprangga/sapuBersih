import os
from pathlib import Path
from src.utility import ResourceManager as util


class JunkFileCleaner:
    def __init__(self, ui_handle):
        self.ui = ui_handle

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

    def scan_temp_files(self, scan_path, patterns, excluded_apps):
        found_files = []
        all_files = self.find_files_by_pattern(scan_path, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:
                found_files.append(file)
        return found_files

    def scan_cache(self, scan_path, patterns, excluded_apps):
        found_files = []
        all_files = self.find_files_by_pattern(scan_path, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:
                found_files.append(file)
        return found_files

    def scan_preferences_for_deleted_apps(self, scan_path, patterns, excluded_apps):
        found_files = []
        all_files = self.find_files_by_pattern(scan_path, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:
                found_files.append(file)
        return found_files

    def exclude_apple_app(self):
        status = self.ui.include_file_checkbox.isChecked()

        paths = set()

        if status:
            paths.update()
        else:
            exclude_apps = util.exclude_apple()
            if exclude_apps:
                paths.update(exclude_apps)
        return list(paths)

    def scan_junk_files(self, preview=True):
        self.ui.clear_tree()

        patterns = ["*"]
        patterns_plist = ["*.plist"]

        if self.ui.include_file_checkbox.isChecked():
            confirm = self.ui.show_question(
                "Are you sure to included Apple applications?"
            )
            if confirm:
                scan_apple_apps = self.exclude_apple_app()
            else:
                self.ui.include_file_checkbox.setChecked(False)
                scan_apple_apps = []
                return
        else:
            scan_apple_apps = self.exclude_apple_app()

        temp_files = self.scan_temp_files(util.temp_paths(), patterns, scan_apple_apps)
        cache_files = self.scan_cache(util.cache_paths(), patterns, scan_apple_apps)
        pref_files = self.scan_preferences_for_deleted_apps(
            util.preference_paths(), patterns_plist, scan_apple_apps
        )

        # Tambahkan file ke UI dengan path lengkap
        for file in temp_files:
            base_name = os.path.basename(file)
            self.ui.add_tree_item(
                base_name, file, "Temporary Files", os.access(file, os.W_OK)
            )

        for cache_dir in cache_files:
            base_name = os.path.basename(cache_dir)
            self.ui.add_tree_item(
                base_name, cache_dir, "Cache Files", os.access(file, os.W_OK)
            )

        for pref_file in pref_files:
            base_name = os.path.basename(pref_file)
            self.ui.add_tree_item(
                base_name, pref_file, "Preference Files", os.access(file, os.W_OK)
            )
