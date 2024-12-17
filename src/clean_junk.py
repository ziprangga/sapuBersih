import os
from pathlib import Path


class JunkFileCleaner:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    def find_files_by_pattern(self, locations, patterns):
        """Temukan file berdasarkan pola dalam lokasi tertentu."""
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

    def clear_temp_files(self, preview=True):
        temp_locations = ["/tmp"]
        patterns = ["*"]  # Semua file
        return self.find_files_by_pattern(temp_locations, patterns)

    def clear_cache(self, preview=True):
        cache_locations = ["/Library/Caches", str(Path.home() / "Library/Caches")]
        patterns = ["*"]  # Semua file/folder di dalam Cache
        return self.find_files_by_pattern(cache_locations, patterns)

    def clear_preferences_for_deleted_apps(self, preview=True):
        preference_locations = [str(Path.home() / "Library/Preferences")]
        patterns = ["*.plist"]  # File .plist
        return self.find_files_by_pattern(preference_locations, patterns)

    def clear_junk_files(self, preview=True):
        self.ui.clear_tree()

        temp_files = self.clear_temp_files(preview=preview)
        cache_files = self.clear_cache(preview=preview)
        pref_files = self.clear_preferences_for_deleted_apps(preview=preview)

        # Tambahkan file ke UI dengan path lengkap
        for file in temp_files:
            base_name = os.path.basename(file)  # Nama file
            self.ui.add_tree_item(
                "Temporary Files", base_name, file, os.access(file, os.W_OK)
            )  # Tambahkan path asli

        for cache_dir in cache_files:
            base_name = os.path.basename(cache_dir)  # Nama folder cache
            self.ui.add_tree_item(
                "Cache Files", base_name, cache_dir, os.access(file, os.W_OK)
            )

        for pref_file in pref_files:
            base_name = os.path.basename(pref_file)  # Nama file preferences
            self.ui.add_tree_item(
                "Preference Files", base_name, pref_file, os.access(file, os.W_OK)
            )
