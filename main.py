import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.main_ui import SapuBersihUI


# Menjalankan Aplikasi
def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = SapuBersihUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
