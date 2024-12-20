import pytest
from PySide6.QtWidgets import QApplication
from src.utility import StyleManager, ResourceManager as util
from gui.main_window import Ui_MainWindow


@pytest.fixture
def qt_app(qtbot):
    qt_app = QApplication.instance() or QApplication([])
    yield qt_app
    qt_app.quit()


def test_apply_dark_qss(qt_app):
    window = Ui_MainWindow()
    StyleManager.apply_stylesheet(window, util.qss_dark_path(), util.qss_light_path())


def test_apply_light_qss(qt_app):
    window = Ui_MainWindow()
    StyleManager.apply_stylesheet(window, util.qss_dark_path(), util.qss_light_path())
