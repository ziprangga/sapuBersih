from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class AboutUI(QDialog):
    def __init__(self, parent=None, app_name="", app_version="", description_text=""):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(400, 300)
        self.setWindowModality(Qt.ApplicationModal)

        # Layout setup
        layout = QVBoxLayout()

        # Application name and version
        app_name_label = QLabel(app_name)
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        version_label = QLabel(app_version)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 14px;")

        # Description
        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-size: 12px;")

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Add widgets to layout
        layout.addWidget(app_name_label)
        layout.addWidget(version_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(close_button)

        self.setLayout(layout)
