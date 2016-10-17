# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/chooselist.ui'
#
# Created: Fri Jul 11 15:08:04 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ChooseListDialog(object):
    def setupUi(self, ChooseListDialog):
        ChooseListDialog.setObjectName(_fromUtf8("ChooseListDialog"))
        ChooseListDialog.resize(400, 123)
        self.buttonBox = QtGui.QDialogButtonBox(ChooseListDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 80, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(ChooseListDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.text_path = QtGui.QLineEdit(ChooseListDialog)
        self.text_path.setGeometry(QtCore.QRect(10, 40, 331, 26))
        self.text_path.setInputMask(_fromUtf8(""))
        self.text_path.setObjectName(_fromUtf8("text_path"))
        self.label_2 = QtGui.QLabel(ChooseListDialog)
        self.label_2.setGeometry(QtCore.QRect(350, 40, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(ChooseListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChooseListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChooseListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseListDialog)

    def retranslateUi(self, ChooseListDialog):
        ChooseListDialog.setWindowTitle(QtGui.QApplication.translate("ChooseListDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ChooseListDialog", "Name of the HDF file (*.hdf) stored at the folder \"data/lists\"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ChooseListDialog", ".hdf", None, QtGui.QApplication.UnicodeUTF8))

