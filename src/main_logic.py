import os
import subprocess
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QLabel,
    QWidget,
)
from pathlib import Path


class SapuBersihLogic:
    def __init__(self, ui_handle):
        self.ui = ui_handle

    # Proses input aplikasi yang akan di delete
    def browse_application(self, app_path=None):
        """Browse untuk mencari aplikasi .app atau menggunakan drag-and-drop."""
        if app_path:
            # Proses langsung jika path diberikan (drag-and-drop)
            app_name = os.path.basename(app_path).replace(".app", "")
            if self.handle_running_processes(app_name):
                self.clean_application(app_path)
                # Jika proses tidak diizinkan, hentikan eksekusi
            else:
                QMessageBox.critical(
                    self, "Invalid Selection", "Please select a valid .app file."
                )
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
            reply = QMessageBox.question(
                self.ui,
                "Running Processes",
                f"Running processes found:\n\n{chr(10).join(processes)}\n\nKill these processes?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.kill_processes(processes)
                QMessageBox.information(
                    self.ui, "Success", "All selected processes have been killed."
                )
            else:
                QMessageBox.information(
                    self.ui,
                    "Info",
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
                self.ui.show_message(f"Successfully killed process with PID: {pid}")
            except subprocess.CalledProcessError:
                self.ui.show_message(
                    f"Failed to kill process with PID: {pid}. It may have already stopped."
                )

    # Menjalankan perintah pencarian file yang terkait dengan aplikasi
    def clean_application(self, app_path):
        self.ui.clear_tree()

        # Ambil bundle identifier
        bundle_identifier = self.get_bundle_identifier(app_path)
        if not bundle_identifier:
            QMessageBox.critical(self.ui, "Error", "Cannot find app bundle identifier.")
            return

        # Dapatkan nama aplikasi
        app_name = os.path.basename(app_path).replace(".app", "")
        self.find_and_save_bom_logs(app_name, bundle_identifier)

        # Temukan data terkait aplikasi
        related_paths = self.find_app_data(app_name, bundle_identifier)
        related_paths.append(app_path)

        if related_paths:
            for path in related_paths:
                self.ui.add_tree_item(path, os.access(path, os.W_OK))
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
        except subprocess.CalledProcessError:
            return None

    # Pencarian berdasarkan direktori cache (.bom) atau log aplikasi jika ditemukan akan di simpan di desktop
    def find_and_save_bom_logs(self, app_name, bundle_identifier):
        base_path = Path("/private/var/db/receipts")
        paths = []

        # Cari .bom files untuk app_name
        for path in base_path.rglob(f"*{app_name}*.bom"):
            paths.append(str(path))

        # Cari .bom files untuk bundle_identifier
        for path in base_path.rglob(f"*{bundle_identifier}*.bom"):
            paths.append(str(path))

        # Hapus duplikat
        paths = list(set(paths))

        # Jika ada file .bom ditemukan, simpan ke desktop
        if paths:
            print("Saving bill of material logs to desktop…")
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
                    print(f"Saved: {bom_log_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {path}: {e}")
        else:
            print("No .bom files found.")

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

        # Daftar lokasi yang relevan untuk mencari data aplikasi
        locations = [
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
            Path(get_darwin_user_cache_dir()),  # Dari getconf
            Path(get_darwin_user_temp_dir()),  # Dari getconf
        ]

        paths = []

        # Cari berdasarkan app_name dan bundle_identifier di setiap lokasi
        for location in locations:
            if location.exists() and location.is_dir():
                # Mencari file atau folder yang cocok dengan app_name
                for match in location.rglob(f"*{app_name}*"):
                    paths.append(str(match))

                # Mencari file atau folder yang cocok dengan bundle_identifier
                for match in location.rglob(f"*{bundle_identifier}*"):
                    paths.append(str(match))

        # Menyaring hasil untuk menerima lokasi unik saja
        return list(set(paths))

    # Membuka lokasi file yang telah ditemukan dan ada di list
    def open_selected_location(self, item, column):
        selected_path = item.text(0)
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
                QMessageBox.critical(self, "Error", f"Failed to open location: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Path not found: {selected_path}")

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
            QMessageBox.warning(
                self.ui, "No Items", "No files/folders available to move to trash."
            )
            return

        # Konfirmasi dengan pengguna
        confirm_message = (
            f"Move {len(items_to_delete)} selected files/folders to trash?"
            if selected_items
            else f"Move all {len(items_to_delete)} files/folders to trash?"
        )
        confirm = QMessageBox.question(
            self.ui, "Confirmation", confirm_message, QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.No:
            return

        success_items = []
        # success_count = 0
        for item in items_to_delete:
            path = item.text(0)
            if not os.path.exists(path):
                QMessageBox.warning(
                    self.ui, "Invalid Path", f"Path does not exist: {path}"
                )
                continue
            if not os.access(path, os.W_OK):
                QMessageBox.critical(
                    self.ui, "Permission Denied", f"No permission to delete: {path}"
                )
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
                QMessageBox.critical(
                    self.ui,
                    "Error",
                    f"Failed to move to trash: {path}\nError: {str(e)}",
                )
            except Exception as e:
                QMessageBox.critical(
                    self.ui,
                    "Error",
                    f"Unexpected error while deleting: {path}\nError: {str(e)}",
                )

        for item in success_items:
            index = self.ui.tree.indexOfTopLevelItem(item)
            self.ui.tree.takeTopLevelItem(index)

        if success_items:
            QMessageBox.information(
                self.ui,
                "Success",
                f"{len(success_items)} files/folders successfully moved to trash.",
            )
