from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
    QPropertyAnimation,
    QSettings,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
    QGuiApplication,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QMainWindow,
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
import subprocess
import platform
import ctypes
from src.app_menu import MenuBar
from src.utility import ResourceManager as util


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        self.selected_file_label = QLabel(self.centralwidget)
        self.selected_file_label.setObjectName("selected_file_label")
        self.selected_file_label.setAlignment(Qt.AlignLeft)
        self.verticalLayout.addWidget(self.selected_file_label)

        # Checkbox "Include Specific Files or Apps" berada di sebelah kanan
        self.include_file_checkbox = QCheckBox(self.centralwidget)
        self.include_file_checkbox.setObjectName("include_file_checkbox")
        self.include_file_checkbox.setText("Include Apple Application")
        self.include_file_checkbox.setChecked(False)
        self.include_file_checkbox.setStyleSheet("margin-right: 25px;")
        self.verticalLayout.addWidget(
            self.include_file_checkbox, alignment=Qt.AlignRight
        )

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.browse_button = QPushButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.horizontalLayout.addWidget(self.browse_button)

        self.scan_button = QPushButton(self.centralwidget)
        self.scan_button.setObjectName("scan_button")
        self.horizontalLayout.addWidget(self.scan_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree = QTreeWidget(self.centralwidget)
        self.tree.setObjectName("tree")
        self.tree.setAlternatingRowColors(True)
        self.tree.setHeaderHidden(False)

        self.verticalLayout.addWidget(self.tree)

        self.delete_button = QPushButton(self.centralwidget)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.scan_button.setMouseTracking(True)

        self.apply_stylesheet(
            self.centralwidget,
            util.qss_dark_path(),
            util.qss_light_path(),
        )

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "sapuBersih", None)
        )
        self.selected_file_label.setText(
            QCoreApplication.translate("MainWindow", "Selected file: None", None)
        )
        self.browse_button.setText(
            QCoreApplication.translate("MainWindow", "Browse Application", None)
        )
        self.scan_button.setText(
            QCoreApplication.translate("MainWindow", "Scan Junk", None)
        )
        self.tree.setHeaderLabels(
            [
                QCoreApplication.translate("MainWindow", "File/Folder", None),
                QCoreApplication.translate("MainWindow", "Path", None),
                QCoreApplication.translate("MainWindow", "Category", None),
                QCoreApplication.translate("MainWindow", "Status", None),
            ]
        )
        self.delete_button.setText(
            QCoreApplication.translate("MainWindow", "Move to Trash", None)
        )

    def apply_stylesheet(
        self, target=None, stylesheet_path_dark=None, stylesheet_path_light=None
    ):
        """Apply stylesheet based on macOS dark mode detection to the target."""
        if not stylesheet_path_dark or not stylesheet_path_light:
            raise ValueError(
                "Both stylesheet_path_dark and stylesheet_path_light must be provided."
            )

        # Detect macOS dark mode
        is_dark_mode = False
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
            )
            is_dark_mode = result.stdout.strip().lower() == "dark"
        except Exception as e:
            print(f"Error detecting dark mode: {e}")

        # Choose the appropriate stylesheet
        stylesheet_path = (
            stylesheet_path_dark if is_dark_mode else stylesheet_path_light
        )

        try:
            with open(stylesheet_path, "r") as file:
                qss = file.read()

            if target is None:
                # Apply globally using QApplication
                QApplication.instance().setStyleSheet(qss)
            elif isinstance(target, QWidget):
                # Apply to a specific QWidget
                target.setStyleSheet(qss)
            else:
                raise ValueError(
                    "Target must be either None, QWidget, or a QMainWindow instance."
                )
        except FileNotFoundError:
            print(f"Stylesheet file not found: {stylesheet_path}")
        except Exception as e:
            print(f"Error applying stylesheet: {e}")
