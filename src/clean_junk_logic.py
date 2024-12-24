import os
from pathlib import Path
from datetime import datetime, timedelta
from src.utility import ResourceManager as util


class JunkFileCleaner:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    def metadata_file(self, filepath, age_days=30, min_size=0):
        try:
            stats = Path(filepath).stat()
            last_modified = datetime.fromtimestamp(stats.st_mtime)
            file_age = datetime.now() - last_modified

            return file_age > timedelta(days=age_days) and stats.st_size >= min_size
        except FileNotFoundError:
            # File may no longer exist
            return False
        except Exception as e:
            print(f"Error accessing file {filepath}: {e}")
            return False

    def include_apple_app(self):
        status = self.ui.include_file_checkbox.isChecked()
        apple_app_patterns = util.include_apple()
        paths = set()
        if not status:
            # If status is unchecked, exclude Apple app-related patterns
            paths.update(apple_app_patterns)
        else:
            # If status is checked, include Apple app-related patterns
            paths.difference_update(apple_app_patterns)
        return list(paths)

    def find_files_by_pattern(self, locations, patterns):
        # Temukan file berdasarkan pola dalam lokasi tertentu
        found_files = set()
        for location in locations:
            location_path = Path(location)
            self.ui.update_status(
                f"Searching in {location_path}...",
            )
            if location_path.exists() and location_path.is_dir():
                for pattern in patterns:
                    found_files.update(
                        str(match) for match in location_path.rglob(pattern)
                    )
            self.ui.stop_update_status()
        return list(found_files)

    def scan_files(self, scan_paths, patterns, age_days=30, min_size=0):
        junk_files_found = []

        found_files = self.find_files_by_pattern(scan_paths, patterns)

        include_apps = self.include_apple_app()
        for file in found_files:
            if self.metadata_file(file, age_days=age_days, min_size=min_size):
                if any(app_pattern in file for app_pattern in include_apps):
                    continue
                junk_files_found.append(file)

        return junk_files_found

    def add_file_to_ui(self, files, category):
        for file in files:
            base_name = os.path.basename(file)
            writable = os.access(file, os.W_OK)
            # Get the last modified date of the file
            file_path = Path(file)
            last_modified = datetime.fromtimestamp(file_path.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            self.ui.add_tree_item(base_name, file, category, writable, last_modified)

    def scan_junk_files(self):
        self.ui.clear_tree()
        self.ui.status_label.clear()

        patterns = util.gen_patterns()

        if self.ui.include_file_checkbox.isChecked():
            confirm = self.ui.show_question(
                "Are you sure to include Apple applications?"
            )
            if confirm:
                pass
            else:
                self.ui.include_file_checkbox.setChecked(False)
                patterns.extend(util.include_apple())

        path_temp = util.temp_paths() + [util.get_darwin_user_temp_dir(as_path=True)]
        path_cache = util.cache_paths() + [util.get_darwin_user_cache_dir(as_path=True)]
        path_log = util.log_paths()

        temp_files = self.scan_files(path_temp, patterns)
        cache_files = self.scan_files(path_cache, patterns)
        log_files = self.scan_files(path_log, patterns)

        self.add_file_to_ui(temp_files, "Temporary Files")
        self.add_file_to_ui(cache_files, "Cache Files")
        self.add_file_to_ui(log_files, "Log Files")

        # Update the status with the current item count (pilih salah satu)
        total_items = self.ui.tree.topLevelItemCount()
        self.ui.update_status(f"Total items: {total_items}")

        return temp_files + cache_files + log_files
