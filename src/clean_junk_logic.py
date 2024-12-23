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

    def scan_files(self, scan_path, patterns, included_apps):
        found_files = []
        all_files = self.find_files_by_pattern(scan_path, patterns)
        for file in all_files:
            for included in included_apps:
                if included in file:
                    break
            else:
                found_files.append(file)
        return found_files

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

    def add_file_to_ui(self, files, category):
        for file in files:
            base_name = os.path.basename(file)
            writable = os.access(file, os.W_OK)
            self.ui.add_tree_item(base_name, file, category, writable)

    def scan_junk_files(self):
        self.ui.clear_tree()

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

        patterns = ["*"]
        patterns_plist = ["*.plist"]
        path_temp = util.temp_paths()
        path_temp.append(util.get_darwin_user_temp_dir(as_path=True))
        path_cache = util.cache_paths()
        path_cache.append(util.get_darwin_user_cache_dir(as_path=True))
        path_log = util.log_paths()
        path_app_support = util.app_support_paths()
        path_pref = util.preference_paths()

        temp_files = self.scan_files(path_temp, patterns, scan_apple_apps)
        cache_files = self.scan_files(path_cache, patterns, scan_apple_apps)
        log_files = self.scan_files(path_log, patterns, scan_apple_apps)
        app_support_files = self.scan_files(path_app_support, patterns, scan_apple_apps)
        pref_files = self.scan_files(path_pref, patterns_plist, scan_apple_apps)

        self.add_file_to_ui(temp_files, "Temporary Files")
        self.add_file_to_ui(cache_files, "Cache Files")
        self.add_file_to_ui(log_files, "Log Files")
        self.add_file_to_ui(app_support_files, "App Support Files")
        self.add_file_to_ui(pref_files, "Preference Files")

        return temp_files + cache_files + pref_files
