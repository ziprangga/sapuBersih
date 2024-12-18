import os
import subprocess
from PySide6.QtWidgets import QFileDialog
from pathlib import Path
import src.utility as util


class SapuBersihLogic:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    # Proses input aplikasi yang akan di delete
    def browse_application(self, app_path=None):
        self.ui.clear_tree()
        # Browse untuk mencari aplikasi .app atau menggunakan drag-and-drop
        if app_path:
            # Proses langsung jika path diberikan (drag-and-drop)
            app_name = os.path.basename(app_path).replace(".app", "")
            if self.handle_running_processes(app_name):
                self.clean_application(app_path)
                # Jika proses tidak diizinkan, hentikan eksekusi
            else:
                if not Path(app_path).is_dir() or not app_path.endswith(".app"):
                    self.ui.show_error("Selected file is not a valid .app bundle.")
                    return
        else:
            # Logika untuk membuka dialog file
            app_path, _ = QFileDialog.getOpenFileName(
                self.ui, "Select Application", "", "Applications (*.app)"
            )
            if app_path:
                self.ui.set_selected_file(app_path)
                app_name = os.path.basename(app_path).replace(".app", "")
                if self.handle_running_processes(app_name):
                    self.clean_application(app_path)

    # Menjalankan cek aplikasi berjalan & menghentikannya
    def handle_running_processes(self, app_name):
        processes = self.get_running_processes(app_name)
        if processes:
            if self.ui.show_question(
                f"Running processes found:\n\n{chr(10).join(processes)}\n\nKill these processes?",
            ):
                self.kill_processes(processes)
            else:
                self.ui.show_error(
                    "The application is still running. Please close it manually.",
                )
                return False

        return True

    # Cek aplikasi yang berjalan termasuk aplikasi yang akan di delete
    def get_running_processes(self, app_name):
        try:
            output = (
                subprocess.check_output(["pgrep", "-afil", app_name]).decode().strip()
            )
            return output.splitlines()
        except subprocess.CalledProcessError:
            return []

    # Menghentikan aplikasi yang berjalan
    def kill_processes(self, processes):
        for process in processes:
            pid = process.split()[0]
            # komentar ini jika menggunakan fitur sudo
            try:
                subprocess.run(["kill", pid], check=True)
                self.ui.show_message(
                    "Success", f"Successfully killed process with PID: {pid}"
                )
            except subprocess.CalledProcessError:
                self.ui.show_error(
                    f"Failed to kill process with PID: {pid}. It may have already stopped."
                )

    # Menjalankan perintah pencarian file yang terkait dengan aplikasi
    def clean_application(self, app_path):

        # Ambil bundle identifier
        bundle_identifier = self.get_bundle_identifier(app_path)
        if not bundle_identifier:
            self.ui.show_error("Cannot find app bundle identifier.")
            return

        # Dapatkan nama aplikasi
        app_name = os.path.basename(app_path).replace(".app", "")
        self.find_and_save_bom_logs(app_name, bundle_identifier)

        # Temukan data terkait aplikasi
        related_paths = self.find_app_data(app_name, bundle_identifier)
        related_paths.append(app_path)

        if related_paths:
            for path in related_paths:
                self.ui.add_tree_item(
                    app_name, path, bundle_identifier, os.access(path, os.W_OK)
                )
        else:
            self.ui.add_placeholder_item()

    # Untuk mencari file yang terkait dengan aplikasi berdaarkan bundle identifier
    def get_bundle_identifier(self, app_path):
        info_plist_path = Path(app_path) / "Contents" / "Info.plist"
        try:
            output = subprocess.check_output(
                [
                    "/usr/libexec/PlistBuddy",
                    "-c",
                    "Print CFBundleIdentifier",
                    str(info_plist_path),
                ],
                stderr=subprocess.STDOUT,
            )
            return output.decode().strip()
        except subprocess.CalledProcessError as e:
            self.ui.show_error(f"Failed to fetch bundle identifier: {str(e)}")
        except FileNotFoundError as e:
            self.ui.show_error(f"Info.plist not found: {str(e)}")
        return None

    # Pencarian berdasarkan direktori cache (.bom) atau log aplikasi jika ditemukan akan di simpan di desktop
    def find_and_save_bom_logs(self, app_name, bundle_identifier):

        paths = []

        receipt_location = util.receipt_paths()
        # Cari .bom files untuk app_name
        for path in receipt_location:
            if path.exists() and path.is_dir():
                for match in path.rglob(f"*{app_name}*.bom"):
                    paths.append(str(path))

        # Cari .bom files untuk bundle_identifier
        for path in receipt_location:
            if path.exists() and path.is_dir():
                for match in path.rglob(f"*{bundle_identifier}*.bom"):
                    paths.append(str(path))

        # Hapus duplikat
        paths = list(set(paths))

        # Jika ada file .bom ditemukan, simpan ke desktop
        if paths:
            desktop_path = os.path.expanduser(f"~/Desktop/{app_name}")
            os.makedirs(desktop_path, exist_ok=True)

            for path in paths:
                try:
                    bom_log_path = os.path.join(
                        desktop_path, f"{os.path.basename(path)}.log"
                    )
                    with open(bom_log_path, "w") as bom_log_file:
                        # Simpan log BOM menggunakan perintah `lsbom`
                        subprocess.run(
                            ["lsbom", "-f", "-l", "-s", "-p", "f", path],
                            stdout=bom_log_file,
                            check=True,
                        )
                    self.ui.show_message("Info", f"Saved: {bom_log_path}")
                except subprocess.CalledProcessError as e:
                    self.ui.show_error(f"Failed to process BOM log: {str(e)}")
                except FileNotFoundError as e:
                    self.ui.show_error(f"BOM file not found: {str(e)}")
        else:
            self.ui.show_message("Info", "No .bom files found.")

    # Pencarian pada direktori yang terkait
    def find_app_data(self, app_name, bundle_identifier):
        def get_darwin_user_cache_dir():
            result = subprocess.run(
                ["getconf", "DARWIN_USER_CACHE_DIR"], capture_output=True, text=True
            )
            return result.stdout.strip()

        def get_darwin_user_temp_dir():
            result = subprocess.run(
                ["getconf", "DARWIN_USER_TEMP_DIR"], capture_output=True, text=True
            )
            return result.stdout.strip()

        locations = util.scan_associated()
        locations.append(Path(get_darwin_user_cache_dir()))
        locations.append(Path(get_darwin_user_temp_dir()))

        paths = set()

        # Cari berdasarkan app_name dan bundle_identifier di setiap lokasi
        for location in locations:
            self.ui.update_status(f"Searching in {location}...")
            if location.exists() and location.is_dir():
                # Mencari file atau folder yang cocok dengan app_name
                paths.update(str(match) for match in location.rglob(f"*{app_name}*"))

                # Mencari file atau folder yang cocok dengan bundle_identifier
                paths.update(
                    str(match) for match in location.rglob(f"*{bundle_identifier}*")
                )
            self.ui.stop_update_status()
        return list(paths)

    # Membuka lokasi file yang telah ditemukan dan ada di list
    def open_selected_location(self, item, column):
        selected_path = item.text(1)
        if os.path.exists(selected_path):
            try:
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        f'tell application "Finder" to reveal POSIX file "{selected_path}"',
                    ]
                )
                subprocess.run(
                    ["osascript", "-e", 'tell application "Finder" to activate']
                )
            except Exception as e:
                self.ui.show_error(f"Failed to open location: {e}")
        else:
            self.ui.show_error(f"Path not found: {selected_path}")

    # Memindahkan file/folder ke trash secara keseluruhan atau yang dipilih
    def move_to_trash(self):

        # Ambil item yang dipilih
        selected_items = self.ui.tree.selectedItems()
        # Jika tidak ada yang dipilih, ambil semua item
        items_to_delete = (
            selected_items
            if selected_items
            else [
                self.ui.tree.topLevelItem(i)
                for i in range(self.ui.tree.topLevelItemCount())
            ]
        )

        if not items_to_delete:
            self.ui.show_message(
                "No Items", "No files/folders available to move to trash."
            )
            return

        # Konfirmasi dengan pengguna
        confirm_message = (
            f"Move {len(items_to_delete)} selected files/folders to trash?"
            if selected_items
            else f"Move all {len(items_to_delete)} files/folders to trash?"
        )
        confirm = self.ui.show_question(confirm_message)
        if confirm:

            success_items = []
            # success_count = 0
            for item in items_to_delete:
                path = item.text(1)
                if not os.path.exists(path):
                    self.ui.show_error(f"Path does not exist: {path}")
                    continue
                if not os.access(path, os.W_OK):
                    self.ui.show_error(f"Permission Denied: {path}")
                    continue

                try:
                    # Kirim file/folder ke Trash menggunakan AppleScript
                    subprocess.run(
                        [
                            "osascript",
                            "-e",
                            f'tell application "Finder" to delete POSIX file "{path}"',
                        ],
                        check=True,
                    )
                    success_items.append(item)  # Tambahkan item ke daftar keberhasilan
                    # success_count += 1
                except subprocess.CalledProcessError as e:
                    self.ui.show_error(
                        f"Failed to move to trash: {path}\nError: {str(e)}",
                    )
                except Exception as e:
                    self.ui.show_error(
                        f"Unexpected error while deleting: {path}\nError: {str(e)}",
                    )
        else:
            return

        for item in success_items:
            index = self.ui.tree.indexOfTopLevelItem(item)
            self.ui.tree.takeTopLevelItem(index)

        if success_items:
            self.ui.show_message(
                "Success",
                f"{len(success_items)} files/folders successfully moved to trash.",
            )
