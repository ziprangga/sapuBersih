# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "sapuBersih", None)
        )
        self.selected_file_label.setText(
            QCoreApplication.translate("MainWindow", "Selected file: None", None)
        )
        self.browse_button.setText(
            QCoreApplication.translate("MainWindow", "Browse", None)
        )
        self.scan_button.setText(QCoreApplication.translate("MainWindow", "Scan", None))
        self.tree.setHeaderLabels(
            [
                QCoreApplication.translate("MainWindow", "File/Folder Path", None),
                QCoreApplication.translate("MainWindow", "Status", None),
            ]
        )
        self.delete_button.setText(
            QCoreApplication.translate("MainWindow", "Move to Trash", None)
        )

    # retranslateUi
