# # -*- coding: utf-8 -*-
import sys

import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QMenu


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 666)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Log Output"))
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)

        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setObjectName("save")
        self.save.setText("Save")
        self.save.move(564, 5)
        self.text = QtWidgets.QTextEdit(self.centralwidget)
        self.text.setObjectName("Text")
        self.text.setGeometry(QtCore.QRect(1, 30, 0, 0))
        self.text.resize(647, 635)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setFixedSize(650, 666)
    Form.setWindowIcon(qtawesome.icon("ri.printer-fill", color='red'))
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())