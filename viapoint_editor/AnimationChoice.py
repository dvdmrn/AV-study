# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnimationChoice.ui'
#
# Created: Fri Jun 20 15:36:36 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AnimationDialog(object):
    def setupUi(self, AnimationDialog):
        AnimationDialog.setObjectName(_fromUtf8("AnimationDialog"))
        AnimationDialog.resize(325, 200)
        self.buttonBox = QtGui.QDialogButtonBox(AnimationDialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 150, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.wavType = QtGui.QRadioButton(AnimationDialog)
        self.wavType.setGeometry(QtCore.QRect(30, 50, 191, 21))
        self.wavType.setChecked(True)
        self.wavType.setObjectName(_fromUtf8("wavType"))
        self.label = QtGui.QLabel(AnimationDialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 271, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.hdfType = QtGui.QRadioButton(AnimationDialog)
        self.hdfType.setGeometry(QtCore.QRect(30, 80, 181, 21))
        self.hdfType.setObjectName(_fromUtf8("hdfType"))
        self.noneType = QtGui.QRadioButton(AnimationDialog)
        self.noneType.setEnabled(False)
        self.noneType.setGeometry(QtCore.QRect(30, 110, 221, 21))
        self.noneType.setObjectName(_fromUtf8("noneType"))

        self.retranslateUi(AnimationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnimationDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnimationDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AnimationDialog)

    def retranslateUi(self, AnimationDialog):
        AnimationDialog.setWindowTitle(QtGui.QApplication.translate("AnimationDialog", "Animation choice", None, QtGui.QApplication.UnicodeUTF8))
        self.wavType.setText(QtGui.QApplication.translate("AnimationDialog", "Using data from audio (WAV) file.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AnimationDialog", "How would you like to generate your animation?", None, QtGui.QApplication.UnicodeUTF8))
        self.hdfType.setText(QtGui.QApplication.translate("AnimationDialog", "Using a HDF file...", None, QtGui.QApplication.UnicodeUTF8))
        self.noneType.setText(QtGui.QApplication.translate("AnimationDialog", "I won\'t generate animation for this file.", None, QtGui.QApplication.UnicodeUTF8))

