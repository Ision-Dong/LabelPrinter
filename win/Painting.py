import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *


class Painter(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 666)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Label Review"))
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Painter()
    widget.show()
    sys.exit(app.exec_())
