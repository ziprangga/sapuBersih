from PySide6.QtWidgets import (
    QMenuBar,
    QMessageBox,
    QCheckBox,
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextBrowser,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from src.utility import resource_path


# Menu Bar
class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        # Membuat menu Help
        help_menu = self.addMenu("Help")

        # Menambahkan item "About"
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_credits)
        help_menu.addAction(about_action)

    def show_credits(self):
        # Path file .txt
        file_path = resource_path("resources/credits.txt")

        try:
            # Membaca isi file
            with open(file_path, "r", encoding="utf-8") as file:
                message = file.read()

            # Menampilkan QMessageBox dengan isi file
            QMessageBox.information(self.parent(), "Credits", message)
        except FileNotFoundError:
            QMessageBox.warning(self.parent(), "Error", "File not found: " + file_path)
        except Exception as e:
            QMessageBox.critical(self.parent(), "Error", f"An error occurred: {e}")
