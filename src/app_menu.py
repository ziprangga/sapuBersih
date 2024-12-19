from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
import src.utility as util
from gui.about_window import AboutUI


# Menu Bar
class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        app_menu = self.addMenu("About")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_ui)
        app_menu.addAction(about_action)

    def show_about_ui(self):
        app_name = "sapuBersih"
        app_version = "Version: 1.1.0"
        author_text = "Author: zi\n\n"
        description_text = author_text
        file_path = util.resource_path("resources/credits.txt")
        try:

            with open(file_path, "r", encoding="utf-8") as file:
                credits_content = file.read()
                description_text += f"{credits_content}"
        except FileNotFoundError:
            description_text += "Credits:\nFile not found: resources/credits.txt"
        except Exception as e:
            description_text += f"Credits:\nAn error occurred: {e}"

        logo_path = util.resource_path("resources/sapuBersih.icns")
        logo_icon = QIcon(logo_path)

        self.about_dialog = AboutUI(
            self, app_name, app_version, description_text, logo_icon
        )

        self.about_dialog.closeRequested.connect(self.on_about_close)
        self.about_dialog.exec()

    def on_about_close(self):
        if self.about_dialog is not None and self.about_dialog.isVisible():
            self.about_dialog.close()
        self.setFocus()
