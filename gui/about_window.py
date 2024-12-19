from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon


class AboutUI(QDialog):
    closeRequested = Signal()

    def __init__(
        self,
        parent=None,
        app_name="",
        app_version="",
        description_text="",
        logo_path="",
    ):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(500, 700)
        self.setWindowModality(Qt.ApplicationModal)

        # Layout setup
        layout = QVBoxLayout()

        # Load and set logo using QIcon
        logo_icon = QIcon(logo_path)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_icon.pixmap(128))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

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
        description_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        description_label.setStyleSheet("font-size: 12px; padding: 5px;")

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.on_close_requested)

        # Add widgets to layout
        layout.addWidget(app_name_label)
        layout.addWidget(version_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(close_button)

        self.setLayout(layout)

    def on_close_requested(self):
        """Emit the closeRequested signal when the button is clicked."""
        self.closeRequested.emit()
