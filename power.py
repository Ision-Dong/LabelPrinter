# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys
import threading
import time
from PyQt5.QtCore import Qt as Q
import qtawesome
# Form implementation generated from reading ui file 'power.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

lock = threading.Lock()


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QLabel, QPushButton, QMessageBox


class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(417, 129)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 40, 311, 48))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.qpushbutton = QtWidgets.QPushButton(self.widget)
        self.qpushbutton.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.qpushbutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.is_show = False
        self.is_auth = False
        self.unique_thread = None
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Power"))
        self.label.setText(_translate("Form", "LockID:"))
        self.label_2.setText(_translate("Form", "            "))
        self.pushButton.setIcon(qtawesome.icon("mdi.cursor-default-click", color='gray', color_active="red"))
        self.pushButton.setIconSize(Qt.QSize(20, 20))
        self.qpushbutton.setIcon(qtawesome.icon("ph.eye-closed-bold", color='gray'))
        self.qpushbutton.setToolTip("Click here to set password to Visible or not.")
        self.qpushbutton.setText("                             ")
        self.qpushbutton.setStyleSheet(
            """
            QPushButton {
                border: 0px;
            }
            """
        )
        self.pushButton.setStyleSheet(
            """
            QPushButton {
                border: 0px;
                background-color: transparent;
            }
            """
        )
        self.lineEdit_2.setVisible(False)
        self.pushButton.clicked.connect(self.run)
        self.qpushbutton.clicked.connect(self.click)

    def click(self):
        if not self.is_show:
            self.qpushbutton.setIcon(qtawesome.icon("ph.eye-bold", color='gray'))
            self.is_show = True
        else:
            self.qpushbutton.setIcon(qtawesome.icon("ph.eye-closed-bold", color='gray'))
            self.is_show = False

    def throw_message(self, message=None):

        messageBox = QMessageBox(QMessageBox.Icon(3), "Error", message, QMessageBox.Ok, self)
        reply = messageBox.exec()
        if reply == QMessageBox.Ok:
            return

    def run(self):
        content = self.lineEdit.text()

        if not self.is_auth:

            if not self.is_show:
                password, ok = QInputDialog.getText(self, 'PASSWORD', 'Please enter your password:', QLineEdit.Password)
            else:
                password, ok = QInputDialog.getText(self, 'PASSWORD', 'Please enter your password:', QLineEdit.Normal)

            date = datetime.datetime.now()
            get_password = "pass" + str(date.month) + "word" + str(date.day)

            if ok:
                if password != get_password:
                    message = "Your password was wrong! \n Please retry."
                    messageBox = QMessageBox(QMessageBox.Icon(3), "Error", message, QMessageBox.Ok, self)
                    reply = messageBox.exec()
                    if reply == QMessageBox.Ok:
                        self.run()
                else:
                    self.is_auth = True
            else:
                return
            return

        self.pushButton.setDisabled(True)
        # check each bit
        for bit in content:
            if bit > "F" and bit > "f":
                self.throw_message( "A bit out of range!")
                return

        if len(content) != 24:
            message = "Commands lenght too large or too less. \nPlease check."
            self.throw_message(message)
            return

        if "," in content:
            content = content.replace(",", " ")

        if self.is_auth:
            self.qpushbutton.setVisible(False)

        content = content[:8] + " " + content[8:16] + " " + content[16:]

        output = os.popen("power.exe {}".format(content))
        content = output.read()
        value = re.findall(r"PN Number:(.+)", content)[0].strip()
        self.lineEdit_2.setVisible(True)
        self.lineEdit_2.setText(value)

        self.thread()

        self.pushButton.setDisabled(False)

    def thread(self):
        if self.unique_thread is None:
            t = threading.Thread(target=self.duration)
            t.start()
            self.unique_thread = t

    def duration(self):
        d = 10
        lock.acquire()
        while d:
            self.pushButton.setText(str(d))
            time.sleep(1)
            d -= 1
        self.lineEdit_2.setVisible(False)
        self.pushButton.setText("")
        lock.release()
        self.unique_thread = None


if __name__ == '__main__':
    QGuiApplication.setAttribute(Q.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.setFixedSize(400, 110)
    widget.setWindowIcon(qtawesome.icon("msc.terminal-powershell", color='red'))
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())