import os
import gui.main_window
from PySide6.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
    QMessageBox,
    QTreeWidget,
    QFileIconProvider,
    QLabel,
    QApplication,
)
from PySide6.QtCore import Qt, QFileInfo, QTimer
from PySide6.QtGui import QIcon, QPixmap
from src.clean_app_logic import SapuBersihLogic
from src.clean_junk_logic import JunkFileCleaner
from src.app_menu import MenuBar
from src.utility import ResourceManager as util


# User Interface
class SapuBersihUI(QMainWindow, gui.main_window.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Atur ikon aplikasi
        icon_path = util.icon_path()
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setWindowIcon(QIcon(icon))
        else:
            self.setWindowIcon(QIcon())

        # Inisialisasi logika
        self.logic = SapuBersihLogic(self)
        self.junk_clean = JunkFileCleaner(self)

        # Atur menu bar
        self.setMenuBar(MenuBar(self))

        self.status_label = QLabel()
        self.stop_update = False
        # self.total_items = 0

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(self.status_label)

        # Menghubungkan sinyal ke slot
        self.browse_button.clicked.connect(self.logic.browse_application)
        self.scan_button.clicked.connect(self.junk_clean.scan_junk_files)
        self.delete_button.clicked.connect(self.logic.move_to_trash)

        # Hubungkan klik dua kali pada item
        self.tree.itemDoubleClicked.connect(self.logic.open_selected_location)
        # multi selection
        self.tree.setSelectionMode(QTreeWidget.MultiSelection)

        # Mengubah cursor ketika berada di atas tombol browse
        if self.browse_button:
            self.browse_button.setCursor(Qt.PointingHandCursor)

        # Aktifkan drop event untuk window
        self.setAcceptDrops(True)

        # Checkbox event click
        self.include_file_checkbox.stateChanged.connect(self.on_checkbox_click)

    # Drag n Drop
    def dragEnterEvent(self, event):
        # Event saat drag masuk ke window
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # Cek/validasi .app
    def is_valid_app_path(self, path):
        return os.path.isdir(path) and path.endswith(".app")

    # Menangkap .app saat drop
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = [url.toLocalFile().strip() for url in event.mimeData().urls()]
            for path in paths:
                path = path.rstrip("/")
                if self.is_valid_app_path(path):
                    self.logic.browse_application(app_path=path)
                else:
                    QMessageBox.warning(
                        self, "Unsupported File", f"'{path}' is not a valid .app file."
                    )
            event.acceptProposedAction()
        else:
            event.ignore()

    # Selected file/folder
    def set_selected_file(self, file_path):
        self.selected_file_label.setText(f"Selected: {file_path}")

    # Membersihkan list
    def clear_tree(self):
        self.tree.clear()

    def add_tree_item(self, name, path, category, writable):
        status = "Accessible" if writable else "Read-Only"

        # Menggunakan QFileIconProvider untuk mendapatkan ikon file atau direktori
        icon_provider = QFileIconProvider()
        file_info = QFileInfo(path)

        # Tentukan apakah path adalah direktori atau file
        if file_info.isDir():
            icon = icon_provider.icon(QFileIconProvider.Folder)
        else:
            icon = icon_provider.icon(QFileIconProvider.File)

        item = QTreeWidgetItem([name, path, category, status])
        item.setIcon(0, icon)
        self.tree.addTopLevelItem(item)

    def remove_tree_item(self, item):
        if item:
            index = self.tree.indexOfTopLevelItem(item)
            if index != -1:
                self.tree.takeTopLevelItem(index)
                # Decrement total_items counter and update status
                self.total_items -= 1
                self.update_status(f"Total items: {self.total_items}")

    def update_status(
        self, message, interval=None, duration=None, immediate_clear=False
    ):

        interval = interval if interval is not None else 3000
        duration = duration if duration is not None else 10000
        self.stop_update = False
        self.process_running = True
        elapsed_time = 0
        self.timer = QTimer(self)

        # Function to update the status at each interval
        def update_message():
            nonlocal elapsed_time
            if self.stop_update or not self.process_running or elapsed_time >= duration:
                self.timer.stop()
                if immediate_clear:
                    self.status_label.clear()
            else:
                elapsed_time += interval
                self.status_label.setText(message)
                QApplication.processEvents()

        # Set up the timer to call `update_message` at regular intervals
        if self.process_running:
            self.timer.timeout.connect(update_message)
            self.timer.start(interval)

        # Immediately show the initial message
        self.status_label.setText(message)
        QApplication.processEvents()

    def stop_update_status(self, clear_immediately=True):
        self.process_running = False
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()
        self.stop_update = True
        if clear_immediately:
            self.status_label.clear()

    # Peletakan Item
    def add_placeholder_item(self):
        item = QTreeWidgetItem(["No files or folders found.", ""])
        item.setFlags(Qt.ItemIsEnabled)
        self.tree.addTopLevelItem(item)

    # Set window icon for QMessageBox and QDialog
    def show_message(self, title, message, icon=QMessageBox.Information):
        QMessageBox(icon, title, message, QMessageBox.Ok, self).exec()

    def show_error(self, message):
        self.show_message("Error", message, QMessageBox.Critical)

    def show_question(self, message, default=QMessageBox.No):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            message,
            QMessageBox.Yes | QMessageBox.No,
            default,
        )
        return reply == QMessageBox.Yes

    def show_log(self, message):
        self.show_message("Log", message)

    def on_checkbox_click(self, state):
        if state == 2:
            return True
        elif state == 0:
            return False
