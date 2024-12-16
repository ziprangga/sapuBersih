import sys
from PySide6.QtWidgets import QApplication
from src.main_ui import SapuBersihUI


# Menjalankan Aplikasi
def main():
    app = QApplication(sys.argv)
    window = SapuBersihUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
