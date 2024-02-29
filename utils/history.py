from PyQt5 import QtCore, QtGui, QtWidgets

from db.sqlite import DBConnector


# QLineEdit添加历史记录功能，按下回车添加至历史中。
class LineEditWithHistory(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super(LineEditWithHistory, self).__init__(parent)

        #   QLineEdit 历史回显功能。
        #   回显数据来源于数据库的MODEL_CODE字段， 当为新用户时，数据库中没有数据，则历史回显为空
        self.db = DBConnector()
        self.inputList = []
        self.db.select()
        for code in self.db.datas:
            if code[1]:
                self.inputList.append(code[1])

        self.completer = QtWidgets.QCompleter(self)
        self.completer.setMaxVisibleItems(10)
        self.listModel = QtCore.QStringListModel(self.inputList, self)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setModel(self.listModel)
        self.completer.activated.connect(self.Slot_completer_activated)
        self.setCompleter(self.completer)

        # 输入完成按下回车后去重添加到历史记录中
        self.editingFinished.connect(self.Slot_editingFinished)

    def Slot_editingFinished(self):
        content = self.text()
        if content != "":
            if content not in self.inputList:
                self.inputList.append(content)
                self.listModel.setStringList(self.inputList)
                self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def Slot_completer_activated(self, text):
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
            self.completer.complete()
            self.completer.popup().show()
            return True
        return super().event(event)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
            self.completer.complete()
            self.completer.popup().show()

