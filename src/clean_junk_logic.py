import os
from pathlib import Path
import src.utility as util


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

    def scan_temp_files(self, preview=True):
        temp_locations = util.temp_paths()
        patterns = ["*"]  # Semua file
        excluded_apps = util.exclude_apps()
        found_files = []
        all_files = self.find_files_by_pattern(temp_locations, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:  # Tidak ditemukan di daftar exclude
                found_files.append(file)
        return found_files

    def scan_cache(self, preview=True):
        cache_locations = util.cache_paths()
        patterns = ["*"]  # Semua file/folder di dalam Cache
        excluded_apps = util.exclude_apps()
        found_files = []
        all_files = self.find_files_by_pattern(cache_locations, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:  # Tidak ditemukan di daftar exclude
                found_files.append(file)
        return found_files

    def scan_preferences_for_deleted_apps(self, preview=True):
        preference_locations = util.preference_paths()
        patterns = ["*.plist"]  # File .plist
        excluded_apps = util.exclude_apps()
        found_files = []
        all_files = self.find_files_by_pattern(preference_locations, patterns)
        for file in all_files:
            for excluded in excluded_apps:
                if excluded in file:
                    break
            else:  # Tidak ditemukan di daftar exclude
                found_files.append(file)
        return found_files

    def scan_junk_files(self, preview=True):
        self.ui.clear_tree()

        temp_files = self.scan_temp_files(preview=preview)
        cache_files = self.scan_cache(preview=preview)
        pref_files = self.scan_preferences_for_deleted_apps(preview=preview)

        # Tambahkan file ke UI dengan path lengkap
        for file in temp_files:
            base_name = os.path.basename(file)  # Nama file
            self.ui.add_tree_item(
                base_name, file, "Temporary Files", os.access(file, os.W_OK)
            )  # Tambahkan path asli

        for cache_dir in cache_files:
            base_name = os.path.basename(cache_dir)  # Nama folder cache
            self.ui.add_tree_item(
                base_name, cache_dir, "Cache Files", os.access(file, os.W_OK)
            )

        for pref_file in pref_files:
            base_name = os.path.basename(pref_file)  # Nama file preferences
            self.ui.add_tree_item(
                base_name, pref_file, "Preference Files", os.access(file, os.W_OK)
            )
