import sys
from PySide6.QtWidgets import QApplication, QMainWindow


def is_dark_mode():
    # Periksa apakah tema gelap sedang aktif
    return QApplication.style().objectName() == "Fusion"
