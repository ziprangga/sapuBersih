from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtGui import QAction
import src.utility as util
from pathlib import Path
from gui.about_window import AboutUI


# Menu Bar
class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        app_menu = self.addMenu("About")

        # Membuat menu about
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_ui)
        app_menu.addAction(about_action)

        # Add "Credits" action
        credits_action = QAction("Credits", self)
        credits_action.triggered.connect(self.show_credits)
        app_menu.addAction(credits_action)

    def show_about_ui(self):
        # Application name and version
        app_name = "sapuBersih"
        app_version = "Version: 1.0.0"

        # Author information
        author_text = "Author: Your Name\n"

        # Base description
        description_text = "sapuBersih is an application designed to make your life easier by helping you manage your tasks efficiently.\n\n"

        # Path to credits file
        file_path = Path("resources/credits.txt")
        try:
            # Read the contents of the file
            with open(file_path, "r", encoding="utf-8") as file:
                credits_content = file.read()
                description_text += f"Credits:\n{credits_content}"
        except FileNotFoundError:
            description_text += "Credits:\nFile not found: resources/credits.txt"
        except Exception as e:
            description_text += f"Credits:\nAn error occurred: {e}"

        # Append author to description
        description_text = author_text + description_text

        # Display the About dialog with dynamic app_name and app_version
        about_dialog = AboutUI(self, app_name, app_version, description_text)
        about_dialog.exec()

    def show_credits(self):
        # Path file .txt
        file_path = util.resource_path("resources/credits.txt")
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
