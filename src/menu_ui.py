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

    #     # Tambahkan checkbox untuk setting
    #     self.checkbox_sudo = QCheckBox("Use sudo to kill processes", self)
    #     self.checkbox_sudo.setChecked(False)

    # def is_sudo_checked(self):
    #     return self.checkbox_sudo.isChecked()

    def init_menu(self):
        # Membuat menu Help
        help_menu = self.addMenu("Help")

        # Menambahkan item "About"
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_credits)
        help_menu.addAction(about_action)

        # # Menambahkan item ke menu Setting
        # preferences_action = QAction("Preferences", self)
        # preferences_action.triggered.connect(self.show_preferences)
        # help_menu.addAction(preferences_action)

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


#     def show_preferences(self):
#         # Membuka dialog Preferences
#         preferences_dialog = PreferencesDialog(self.parent())
#         preferences_dialog.exec()


# class PreferencesDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Preferences")
#         self.setFixedSize(300, 200)

#         # Layout untuk checkbox
#         layout = QVBoxLayout(self)

#         # Tambahkan checkbox
#         self.checkbox = QCheckBox("Enable Advanced Options", self)
#         self.checkbox.setChecked(False)  # Default tidak dicentang
#         self.checkbox.stateChanged.connect(self.update_status)
#         layout.addWidget(self.checkbox)

#         # Tambahkan label di bawah checkbox pertama
#         self.label_advanced = QTextBrowser(self)
#         self.label_advanced.setText(
#             "This option enables/disable Admin priviledge, use only for kill application process that need Admin priviledge(sudo). By default always try not using admin priviledge (sudo)",
#         )
#         # self.label_advanced.setStyleSheet("color: gray; font-size: 12px;")
#         layout.addWidget(self.label_advanced)

#         # Tambahkan label untuk menampilkan status
#         self.status_label = QLabel(self)
#         layout.addWidget(self.status_label)

#     def update_status(self, state):
#         sender = self.sender()
#         if sender == self.checkbox:
#             if state:
#                 self.status_label.setText("Admin priviledge : Enabled")
#             else:
#                 self.status_label.setText("Admin priviledge: Disabled")
