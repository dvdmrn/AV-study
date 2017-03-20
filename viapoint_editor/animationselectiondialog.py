# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AnimationSelectionDialog.ui'
#
# Created: Wed Jul 23 10:56:34 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AnimationSelectionDialog(object):
    def setupUi(self, AnimationSelectionDialog):
        AnimationSelectionDialog.setObjectName(_fromUtf8("AnimationSelectionDialog"))
        AnimationSelectionDialog.resize(273, 295)
        self.buttonBox = QtGui.QDialogButtonBox(AnimationSelectionDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 250, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.list_animations = QtGui.QListWidget(AnimationSelectionDialog)
        self.list_animations.setGeometry(QtCore.QRect(10, 40, 251, 201))
        self.list_animations.setObjectName(_fromUtf8("list_animations"))
        self.label = QtGui.QLabel(AnimationSelectionDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(AnimationSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnimationSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnimationSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnimationSelectionDialog)

    def retranslateUi(self, AnimationSelectionDialog):
        AnimationSelectionDialog.setWindowTitle(QtGui.QApplication.translate("AnimationSelectionDialog", "Animation selection", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AnimationSelectionDialog", "Select animation file", None, QtGui.QApplication.UnicodeUTF8))

