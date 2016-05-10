# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatasetDialog.ui'
#
# Created: Wed Jun 25 11:08:53 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DatasetDialog(object):
    def setupUi(self, DatasetDialog):
        DatasetDialog.setObjectName(_fromUtf8("DatasetDialog"))
        DatasetDialog.resize(400, 295)
        self.buttonBox = QtGui.QDialogButtonBox(DatasetDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.datalist = QtGui.QListWidget(DatasetDialog)
        self.datalist.setGeometry(QtCore.QRect(10, 40, 381, 191))
        self.datalist.setObjectName(_fromUtf8("datalist"))
        self.label = QtGui.QLabel(DatasetDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(DatasetDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DatasetDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DatasetDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DatasetDialog)

    def retranslateUi(self, DatasetDialog):
        DatasetDialog.setWindowTitle(QtGui.QApplication.translate("DatasetDialog", "Dataset Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DatasetDialog", "Select Dataset used as animation", None, QtGui.QApplication.UnicodeUTF8))

