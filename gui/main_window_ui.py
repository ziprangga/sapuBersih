# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.selected_file_label = QLabel(self.centralwidget)
        self.selected_file_label.setObjectName(u"selected_file_label")
        self.selected_file_label.setAlignment(Qt.AlignLeft)

        self.verticalLayout.addWidget(self.selected_file_label)

        self.browse_button = QPushButton(self.centralwidget)
        self.browse_button.setObjectName(u"browse_button")

        self.verticalLayout.addWidget(self.browse_button)

        self.tree = QTreeWidget(self.centralwidget)
        self.tree.setObjectName(u"tree")
        self.tree.setAlternatingRowColors(True)
        self.tree.setHeaderHidden(False)

        self.verticalLayout.addWidget(self.tree)

        self.delete_button = QPushButton(self.centralwidget)
        self.delete_button.setObjectName(u"delete_button")

        self.verticalLayout.addWidget(self.delete_button)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"sapuBersih", None))
        self.selected_file_label.setText(QCoreApplication.translate("MainWindow", u"Selected file: None", None))
        self.browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.tree.setHeaderLabels([
            QCoreApplication.translate("MainWindow", u"File/Folder Path", None),
            QCoreApplication.translate("MainWindow", u"Status", None)])
        self.delete_button.setText(QCoreApplication.translate("MainWindow", u"Move to Trash", None))
    # retranslateUi

