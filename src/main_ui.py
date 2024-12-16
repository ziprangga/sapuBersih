import sys
import os
import gui.main_window
from PySide6.QtWidgets import (
    QMainWindow,
    QTreeWidgetItem,
    QMessageBox,
    QTreeWidget,
    QFileIconProvider,
)
from PySide6.QtCore import Qt, QFileInfo
from PySide6.QtGui import QIcon
from src.main_logic import SapuBersihLogic
from src.menu_ui import MenuBar
from src.utility import resource_path


# User Interface
class SapuBersihUI(QMainWindow, gui.main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Inisialisasi logika
        self.logic = SapuBersihLogic(self)

        # Atur menu bar
        self.setMenuBar(MenuBar(self))

        # Atur ikon aplikasi
        self.setWindowIcon(QIcon(resource_path("resources/sapu_bersih.icns")))

        # Menghubungkan sinyal ke slot
        self.browse_button.clicked.connect(self.logic.browse_application)
        self.delete_button.clicked.connect(self.logic.move_to_trash)

        # Hubungkan klik dua kali pada item
        self.tree.itemDoubleClicked.connect(self.logic.open_selected_location)
        # multi selection
        self.tree.setSelectionMode(QTreeWidget.MultiSelection)

        # Mengubah cursor saat mouse berada di atas tombol browse_button
        self.browse_button.setCursor(
            Qt.PointingHandCursor
        )  # Mengubah cursor menjadi tangan (hand cursor)

        # Mengubah cursor ketika berada di atas tombol browse
        if self.browse_button:
            self.browse_button.setCursor(Qt.PointingHandCursor)

        # Aktifkan drop event untuk window
        self.setAcceptDrops(True)

    # Drag n Drop
    def dragEnterEvent(self, event):
        """Event saat drag masuk ke window."""
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
            paths = [
                url.toLocalFile().strip()
                for url in event.mimeData().urls()
                if url.isLocalFile()
            ]

            for path in paths:
                path = path.rstrip("/")  # Bersihkan trailing slash
                if self.is_valid_app_path(path):
                    self.logic.browse_application(app_path=path)
                else:
                    QMessageBox.warning(
                        self,
                        "Unsupported File",
                        f"'{path}' is not a valid .app file.",
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

    def add_tree_item(self, path, writable):
        status = "Accessible" if writable else "Read-Only"

        # Menggunakan QFileIconProvider untuk mendapatkan ikon file atau direktori
        icon_provider = QFileIconProvider()
        file_info = QFileInfo(path)

        # Tentukan apakah path adalah direktori atau file
        if file_info.isDir():
            icon = icon_provider.icon(QFileIconProvider.Folder)
        else:
            icon = icon_provider.icon(QFileIconProvider.File)

        item = QTreeWidgetItem([path, status])
        item.setIcon(0, icon)  # Gunakan ikon yang didapat dari QFileIconProvider
        self.tree.addTopLevelItem(item)

    # Peletakan Item
    def add_placeholder_item(self):
        item = QTreeWidgetItem(["No files or folders found.", ""])
        item.setFlags(Qt.ItemIsEnabled)
        self.tree.addTopLevelItem(item)
