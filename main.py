import sys

import qtawesome
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from MainWindow import Ui_MainWindow


# The app entrance here.
class RQMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(RQMainWindow, self).__init__(parent)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning',
                                     "Do you want to close all windows?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore()


if __name__ == '__main__':
    styleFile = 'qss/style_v3.qss'

    QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    win = RQMainWindow()
    win.setWindowIcon(qtawesome.icon("ri.printer-fill", color='red'))
    ui = Ui_MainWindow()
    ui.setupUi(win)
    with open(styleFile, "r") as f:
        style = f.read()
    win.setStyleSheet(style)
    f.close()
    win.show()
    sys.exit(app.exec_())




