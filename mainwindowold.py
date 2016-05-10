# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/basic2.ui'
#
# Created: Mon Jul 14 15:53:04 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindowOld(object):
    def setupUi(self, MainWindowOld):
        MainWindowOld.setObjectName(_fromUtf8("MainWindowOld"))
        MainWindowOld.resize(525, 276)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindowOld.sizePolicy().hasHeightForWidth())
        MainWindowOld.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindowOld)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.wavfile = QtGui.QLineEdit(self.centralwidget)
        self.wavfile.setEnabled(True)
        self.wavfile.setGeometry(QtCore.QRect(20, 30, 391, 27))
        self.wavfile.setReadOnly(True)
        self.wavfile.setObjectName(_fromUtf8("wavfile"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 51, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.duration = QtGui.QLabel(self.centralwidget)
        self.duration.setGeometry(QtCore.QRect(20, 70, 141, 17))
        self.duration.setObjectName(_fromUtf8("duration"))
        self.selectfile = QtGui.QPushButton(self.centralwidget)
        self.selectfile.setGeometry(QtCore.QRect(420, 30, 85, 27))
        self.selectfile.setObjectName(_fromUtf8("selectfile"))
        self.animationsizelabel = QtGui.QLabel(self.centralwidget)
        self.animationsizelabel.setGeometry(QtCore.QRect(210, 70, 191, 17))
        self.animationsizelabel.setObjectName(_fromUtf8("animationsizelabel"))
        self.clearanimation = QtGui.QPushButton(self.centralwidget)
        self.clearanimation.setGeometry(QtCore.QRect(200, 190, 131, 27))
        self.clearanimation.setObjectName(_fromUtf8("clearanimation"))
        self.startanimation = QtGui.QPushButton(self.centralwidget)
        self.startanimation.setGeometry(QtCore.QRect(400, 190, 111, 27))
        self.startanimation.setObjectName(_fromUtf8("startanimation"))
        self.plotamplitude = QtGui.QPushButton(self.centralwidget)
        self.plotamplitude.setGeometry(QtCore.QRect(20, 190, 111, 27))
        self.plotamplitude.setObjectName(_fromUtf8("plotamplitude"))
        self.lpffrequency = QtGui.QSpinBox(self.centralwidget)
        self.lpffrequency.setGeometry(QtCore.QRect(210, 100, 81, 27))
        self.lpffrequency.setMaximum(20000)
        self.lpffrequency.setObjectName(_fromUtf8("lpffrequency"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.reloadanimation = QtGui.QPushButton(self.centralwidget)
        self.reloadanimation.setGeometry(QtCore.QRect(20, 140, 491, 27))
        self.reloadanimation.setObjectName(_fromUtf8("reloadanimation"))
        MainWindowOld.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindowOld)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 525, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuParameters = QtGui.QMenu(self.menubar)
        self.menuParameters.setObjectName(_fromUtf8("menuParameters"))
        MainWindowOld.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindowOld)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindowOld.setStatusBar(self.statusbar)
        self.actionEdit = QtGui.QAction(MainWindowOld)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionLoad_from_file = QtGui.QAction(MainWindowOld)
        self.actionLoad_from_file.setObjectName(_fromUtf8("actionLoad_from_file"))
        self.actionSave_file = QtGui.QAction(MainWindowOld)
        self.actionSave_file.setObjectName(_fromUtf8("actionSave_file"))
        self.menuParameters.addAction(self.actionEdit)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionLoad_from_file)
        self.menuParameters.addAction(self.actionSave_file)
        self.menubar.addAction(self.menuParameters.menuAction())

        self.retranslateUi(MainWindowOld)
        QtCore.QMetaObject.connectSlotsByName(MainWindowOld)

    def retranslateUi(self, MainWindowOld):
        MainWindowOld.setWindowTitle(QtGui.QApplication.translate("MainWindowOld", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindowOld", "WAV file", None, QtGui.QApplication.UnicodeUTF8))
        self.duration.setText(QtGui.QApplication.translate("MainWindowOld", "Sound duration: -", None, QtGui.QApplication.UnicodeUTF8))
        self.selectfile.setText(QtGui.QApplication.translate("MainWindowOld", "Select file...", None, QtGui.QApplication.UnicodeUTF8))
        self.animationsizelabel.setText(QtGui.QApplication.translate("MainWindowOld", "Animation data size: -", None, QtGui.QApplication.UnicodeUTF8))
        self.clearanimation.setText(QtGui.QApplication.translate("MainWindowOld", "Clear graphics queue", None, QtGui.QApplication.UnicodeUTF8))
        self.startanimation.setText(QtGui.QApplication.translate("MainWindowOld", "Start animation", None, QtGui.QApplication.UnicodeUTF8))
        self.plotamplitude.setText(QtGui.QApplication.translate("MainWindowOld", "Plot amplitude", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindowOld", "Low pass filter frequency", None, QtGui.QApplication.UnicodeUTF8))
        self.reloadanimation.setText(QtGui.QApplication.translate("MainWindowOld", "Reload Animation", None, QtGui.QApplication.UnicodeUTF8))
        self.menuParameters.setTitle(QtGui.QApplication.translate("MainWindowOld", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("MainWindowOld", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_from_file.setText(QtGui.QApplication.translate("MainWindowOld", "Load from file...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_file.setText(QtGui.QApplication.translate("MainWindowOld", "Export to file", None, QtGui.QApplication.UnicodeUTF8))

