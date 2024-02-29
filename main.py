import sys

import qtawesome
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from MainWindow import Ui_MainWindow


# The app entrance here.
class RQMainWindow(QMainWindow):

    # 重新定义主窗口， 继承自QMainWindow
    # 重新定义主窗口的退出动作， 退出前弹出窗口询问用户是否确定退出
    # 点击yes 按钮，成功退出， 点击no按钮，不退出
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
    # 设置窗口文本自适应
    QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    win = RQMainWindow()
    win.setWindowIcon(qtawesome.icon("ri.printer-fill", color='red'))
    ui = Ui_MainWindow()
    ui.setupUi(win)
    # 从文件中加载QSS样式
    with open(styleFile, "r") as f:
        style = f.read()
    win.setStyleSheet(style)
    f.close()
    win.show()
    sys.exit(app.exec_())




