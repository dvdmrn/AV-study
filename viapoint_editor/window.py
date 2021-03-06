# -*- coding: utf-8 -*-

import os
import sys
import glob
import ntpath

#temporary import.... will be deleted later
from windowold import *

from tables import *

from mainwindow import *
from mainwindowold import *
from parametersdialog import *
from AnimationChoice import *
from DatasetDialog import *
from animationdialog import *

import gizeh
# from moviepy.editor import VideoClip
# from moviepy.editor import AudioFileClip

import numpy as np

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from animationlist import *

from chooselist import *
from animationselectiondialog import *

from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setFixedSize(self.geometry().width(), self.geometry().height())
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        
        self.dialog_chooselist = ChooseListDialog()
        self.dialog_animationselection = AnimationSelectionDialog()
        self.dialog_animation = AnimationDialog(self)

        self.dialog_animation.setupVariablesTable()
        
        self.folder_path = os.path.dirname(os.path.realpath(__file__))
        self.animationList = AnimationList()

        self.listcontextmenu = QMenu()

        self.updateListToolbarStatus()
        self.connectButtons()

    def connectButtons(self):

        #list toolbar
        self.button_up.clicked.connect(self.moveListItemUp)
        self.button_down.clicked.connect(self.moveListItemDown)
        self.button_add.clicked.connect(self.addAnimationToList)
        self.button_remove.clicked.connect(self.removeAnimationFromList)

        #load
        self.menu_load_list.triggered.connect(self.loadAnimationList)
        self.button_load_list.clicked.connect(self.loadAnimationList)

        #save
        self.menu_save_list.triggered.connect(self.saveAnimationListCall)
        self.button_save_list.clicked.connect(self.saveAnimationListCall)

        #new
        self.menu_new_list.triggered.connect(self.newAnimationList)
        self.button_new_list.clicked.connect(self.newAnimationList)

        self.menu_animation_new.triggered.connect(self.createNewAnimation)
        self.menu_animation_edit.triggered.connect(self.openAnimationDialogCall)
        
        #list change
        self.list_list.itemSelectionChanged.connect(self.updateListToolbarStatus)
        self.list_list.doubleClicked.connect(self.listDoubleClicked)

        self.group_player.clicked.connect(self.playerBoxChecked)
        self.button_start.clicked.connect(self.playerButton)

        self.menu_quit.triggered.connect(self.quitAction)

        self.createListMenu()
        self.list_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_list.customContextMenuRequested.connect(self.showListMenu)

    def showListMenu(self, pos):

        menu = self.createListMenu()
        menu.exec_(self.list_list.mapToGlobal(pos))

    def createListMenu(self):

        menu = QMenu(self.list_list)

        move_up = QAction("Move up", menu)
        move_up.triggered.connect(self.moveListItemUp)
        
        move_down = QAction("Move down", menu)
        move_down.triggered.connect(self.moveListItemDown)
        
        remove = QAction("Remove from list", menu)
        remove.triggered.connect(self.removeAnimationFromList)

        edit = QAction("Edit", menu)
        edit.triggered.connect(self.listDoubleClicked)
        
        plot = QAction("Plot", menu)
        plot.triggered.connect(self.plotAnimationFromList)
        
        if (not self.button_down.isEnabled()):
            move_down.setEnabled(False)
            
        if (not self.button_up.isEnabled()):
            move_up.setEnabled(False)
            
        if (not self.button_remove.isEnabled()):
            move_up.setEnabled(False)
            edit.setEnabled(False)
            plot.setEnabled(False)
            remove.setEnabled(False)
            
        menu.addAction(move_up)
        menu.addAction(move_down)
        menu.addAction(remove)
        menu.addSeparator()
        menu.addAction(edit)
        menu.addSeparator()
        menu.addAction(plot)

        return menu

    def plotAnimationFromList(self):
        
        item = self.list_list.currentItem()

        if (not item is None):
            order = self.list_list.currentRow()
            path = self.animationList.getOrderedList()[order].getFile()

            animation = MainAnimation()
            animation.setFile(path)
            animation.loadFile()

            self.dialog_animation.animation = animation
            self.dialog_animation.plotAnimation()
        
    def quitAction(self):

        self.playerStop()
        exit()
        
    def playerBoxChecked(self, checked):
        
        self.group_list.setEnabled(not checked)
        self.menubar.setEnabled(not checked)

        if (checked):
            self.updatePlayerBoxTotalTime()
            
    def createNewAnimation(self):

        animation = MainAnimation()
        animation.createList()
        animation.setName("New Animation")
        
        self.dialog_animation.animation = animation
        self.dialog_animation.updateListControls()
        self.dialog_animation.exec_()

    def listDoubleClicked(self):

        item = self.list_list.currentItem()

        if (not item is None):
            order = self.list_list.currentRow()
            path = self.animationList.getOrderedList()[order].getFile()

            self.openAnimationDialog(path)

    def openAnimationDialogCall(self):

        self.openAnimationDialog()
        
    def openAnimationDialog(self, path=""):
        
        if (path == ""):
            animation_file = self.dialog_animationselection.getAnimationFile()
        else:
            animation_file = path
            
        if (animation_file != ""):

            animation = MainAnimation()
            animation.setFile(animation_file)
            animation.loadFile()

            self.dialog_animation.animation = animation

            self.dialog_animation.updateListControls()
            self.dialog_animation.exec_()

                                                  
    def updateAnimationsList(self):

        selected = self.list_list.currentIndex()
    
        self.list_list.clear()

        if (self.animationList.isLoaded()):
            for name in self.animationList.getOrderedNames():
                self.list_list.addItem(name)     

        self.list_list.setCurrentIndex(selected)

        
    def updateListToolbarStatus(self):

        item = self.list_list.currentItem()
    
        if (self.animationList.isLoaded()):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)
        
        if (item is None):
            self.button_up.setEnabled(False)
            self.button_down.setEnabled(False)
            self.button_remove.setEnabled(False)

            return
        else:
            self.button_up.setEnabled(True)
            self.button_down.setEnabled(True)
            self.button_remove.setEnabled(True)

        index = self.list_list.currentRow()
    
        if (index == self.list_list.count() - 1):
            self.button_down.setEnabled(False)

        if (index == 0):
            self.button_up.setEnabled(False)

    
    def saveAnimationListCall(self):
        
        if (self.animationList.isLoaded()):
            self.saveAnimationList()

        
    def saveAnimationList(self, path=""):

        try:
            self.animationList.saveFile(path)
            self.updateListControls()
        except AnimationListException as e:
            code, message = e.args

            if (code == AnimationListErrors.FILE_EMPTY):
                path = self.dialog_chooselist.getSavePath()
                if (path != ""):
                    self.saveAnimationList(path)
            
            elif (code == AnimationListErrors.NOT_LOADED):
                self.label_queue_name.setText("-")
                self.animationList = AnimationList()
                self.updateAnimationsList()
                self.updateListToolbarStatus()

    def reloadAnimationsFromList(self):

        if (self.animationList.isLoaded()):
            for obj in self.animationList.getList():
                obj.loadFile()

            self.updateListControls()
                
    def loadAnimationList(self):
    
        loadList = AnimationList()

        try:
            loadList.loadFile(self.dialog_chooselist.getSavePath(True))
            self.animationList = loadList
        except AnimationListException as e:
            return
    
        self.updateListControls()

        
    def updateListControls(self):
    
        if (self.animationList.isLoaded()):
            text = self.animationList.getFile()
            if (text == ""):
                text = "* New List *"
            
            self.label_queue_name.setText(text)
            self.button_save_list.setEnabled(True)
            self.menu_save_list.setEnabled(True)
            
        
            self.updateAnimationsList()
            self.updateListToolbarStatus()
            
        else:
            
            self.button_save_list.setEnabled(False)
            self.menu_save_list.setEnabled(False)
            self.label_queue_name.setText("-")


    def updatePlayerBoxTotalTime(self):

        total_time = 0

        for animation in self.animationList.getOrderedList():
            animation.loadWAVFile()
            total_time += animation.getWAVSignal().getTotalSeconds()

        minutes = int(math.floor(total_time/60.0))
        seconds = int(total_time % 60)

        
        self.label_total_time.setText("%02d:%02d" % (minutes, seconds))

            
    def moveListItem(self, down):

        item = self.list_list.currentItem()

        if (not(item is None)):
            index = self.list_list.currentRow()
            if (down):
                self.animationList.moveDown(index)
            else:
                self.animationList.moveUp(index)

            self.updateAnimationsList()
            self.updateListToolbarStatus()

            
    def moveListItemUp(self):
        
        next = max(0, self.list_list.currentRow() - 1)
        self.moveListItem(False)
        self.list_list.setCurrentRow(next)

        
    def moveListItemDown(self):
        
        next = min(self.list_list.count() - 1, self.list_list.currentRow() + 1)
        self.moveListItem(True)
        self.list_list.setCurrentRow(next)

        
    def newAnimationList(self):

        self.animationList = AnimationList()
    
        self.animationList.createList()
        self.updateListControls()


    def addAnimationToList(self):

        if (self.animationList.isLoaded()):

            animation_file = self.dialog_animationselection.getAnimationFile()
    
            if (animation_file != ""):
                animation = MainAnimation()
                animation.setFile(animation_file)
                animation.loadFile()

                self.animationList.addAnimation(animation)
                
                self.updateListControls()

    def removeAnimationFromList(self):

        if (self.animationList.isLoaded()):
            order = self.list_list.currentRow()

            self.animationList.removeAnimationByOrder(order)
            self.updateListControls()

    def onAnimationStart(self):
        
        self.animationList.onAnimationStart()

    def onAnimationExecution(self):

        self.animationList.onAnimationExecution()

    def printLog(self, text):

        self.text_log.appendHtml(str(text))

    def onAnimationFinish(self):

        self.animationList.onAnimationFinish()

        if (not self.animationList.isRunning()):
            self.button_start.setText("Start")
            self.group_player.setCheckable(True)
        
    def playerButton(self):
        print("you clicked on the right button, pal")
        #!!!! os.system the player console
        os.system("python animationplayer/animationPlayerConsole.py")





        #load an animation file

        # if (self.animationList.isRunning()):
        #     self.printLog("Animation execution stopped!")
        #     self.playerStop()
        # else:
        #     self.printLog("Animation execution started!")
        #     self.playerStart()

    def playerStart(self):

        if (self.animationList.isLoaded()):

            self.group_player.setCheckable(False)
            self.button_start.setText("Stop")
            self.animationList.createPlaylist()
            self.animationList.setAnimationsActions(self.onAnimationStart, self.onAnimationExecution, self.onAnimationFinish)
            self.animationList.startPlaylist()


    def playerStop(self):

        if (self.animationList.isLoaded()):
            self.group_player.setCheckable(True)
            self.button_start.setText("Start")
            self.animationList.clearPlaylist()
            
class ChooseListDialog(QDialog, Ui_ChooseListDialog):

    def __init__(self):

        QDialog.__init__(self)
        self.folder_path = os.path.dirname(os.path.realpath(__file__))
        
        self.setupUi(self)

    def getSavePath(self, loading=False, text=""):

        folder_path = self.folder_path + "/data/lists/"
        
        self.text_path.setText(text)
        self.text_path.selectAll()
        self.text_path.setFocus()
        
        self.exec_()

        if (self.result() == 1):
            path = str(self.text_path.text()) + ".hdf"

            if (loading):
                if (os.path.isfile(folder_path + path)):
                    return path
                else:
                    return self.getSavePath(loading, self.text_path.text())

            else:
                if (os.path.isfile(folder_path + path)):
                    question = QMessageBox.Question("File already exist", "This file already exists. Do you really want to continue this operation? All the information stored in the file will be lost.")
                    if (question == QMessageBox.Yes):
                        return path
                    else:
                        return self.getSavePath(loading, self.text_path.text())
                else:
                    return path
        else:
            return ""


class SelectionDialog(QDialog, Ui_AnimationSelectionDialog):

    def __init__(self):

        QDialog.__init__(self)
        self.folder_path = os.path.dirname(os.path.realpath(__file__))
        
        self.setupUi(self)
        self.list_animations.doubleClicked.connect(self.accept)

    def _loadList(self, mask):
        
        folder_mask = self.folder_path + mask
        return [ ntpath.basename(name) for name in glob.glob(folder_mask) ]

    def loadList(self):
        pass
        
    def updateList(self):

        self.list_animations.clear()
        
        for item in self.loadList():
            self.list_animations.addItem(item)

    def getFile(self):

        self.updateList()
        self.exec_()

        if (self.result() == 1):
            item = self.list_animations.currentItem()

            if (not(item is None)):
                return str(item.text())
            else:
                return ""
        else:
            return ""

class AnimationSelectionDialog(SelectionDialog):

    def __init__(self):

        SelectionDialog.__init__(self)

    def loadList(self):

        return self._loadList("/data/animations/*.hdf")

    def getAnimationFile(self):

        return self.getFile()

class WAVSelectionDialog(SelectionDialog):

    def __init__(self):

        SelectionDialog.__init__(self)

    def loadList(self):

        return self._loadList("/data/wav/*.wav")

    def getWAVFile(self):

        return self.getFile()

class SignalSelectionDialog(SelectionDialog):

    def __init__(self):

        SelectionDialog.__init__(self)

    def loadList(self):

        return self._loadList("/data/signals/*.hdf")

    def getHDFFile(self):

        return self.getFile()

class ParameterSelectionDialog(SelectionDialog):
    
    def __init__(self):

        SelectionDialog.__init__(self)

    def loadList(self):

        l = self._loadList("/data/parameters/*.py")
        try:
            l.remove('__init__.py')
        except:
            pass

        return l

    def getParameterFile(self):

        return self.getFile()

class DataSelectionDialog(SelectionDialog):

    def __init__(self):

        SelectionDialog.__init__(self)
        self.hdffile = ""

    def loadList(self):

        return self._loadList(self.hdffile)

    def getBranch(self):

        return self.getFile()

    def setHDFFile(self, path):

        self.hdffile = self.folder_path + "/data/signals/" + path
    
    def _loadList(self, datafile):

        hdf = tables.openFile(datafile, 'r')
        nodes = [node._v_pathname for node in hdf.walkNodes("/", "Array")]
        hdf.close()

        return nodes
    

class AnimationDialog(QDialog, Ui_AnimationDialog):

    def __init__(self,  mainInstance):
        
        QDialog.__init__(self)
        self.setupUi(self)

        self.setFixedSize(self.geometry().width(), self.geometry().height())

        self.animation = MainAnimation()

        self.main_window = mainInstance
        
        self.dialog_parameterselection = ParameterSelectionDialog()
        self.dialog_wavselection = WAVSelectionDialog()
        self.dialog_signalselection = SignalSelectionDialog()
        self.dialog_dataselection = DataSelectionDialog()
        
        self.folder_path = os.path.dirname(os.path.realpath(__file__))

        self.connectButtons()

    def closeEvent(self, event):

        event.ignore()
        
    def connectButtons(self):

        #list toolbar buttons
        self.button_up.clicked.connect(self.moveListItemUp)
        self.button_down.clicked.connect(self.moveListItemDown)
        self.button_add.clicked.connect(self.addParameterToList)
        self.button_remove.clicked.connect(self.removeParameterFromList)

        #state change
        self.list_list.itemSelectionChanged.connect(self.updateListToolbarStatus)
        self.check_signal.stateChanged.connect(self.changedAnimationType)

        #dialog buttons
        self.label_animation_name.clicked.connect(self.changeAnimationName)
        self.button_audio.clicked.connect(self.selectAnimationAudio)
        self.button_signal.clicked.connect(self.selectAnimationSignal)
        self.button_plot.clicked.connect(self.plotAnimation)
        self.button_export.clicked.connect(self.exportAnimation)
        self.button_play_test.clicked.connect(self.playTest)
        self.button_select_data.clicked.connect(self.selectAnimationBranch)
        self.button_interaction.clicked.connect(self.callInteraction)
    
        buttonSave = self.buttonBox.button(QDialogButtonBox.Save)
        buttonSave.clicked.disconnect()
        buttonSave.clicked.connect(self.saveAnimation)

    def callInteraction(self):

        index = self.list_list.currentRow()
        parameter = self.animation.getOrderedList()[index]

        self.animation.initializeAnimation()
        self.animation.loadAnimation(stopParameter=parameter)

        parameter.interaction(self.animation.signal.getData(), self.animation.signal.getAnimationData(), self.animation.wavsignal.getData(), self)

        self.updateVariablesTable()
        
    def selectAnimationBranch(self):

        self.dialog_dataselection.setHDFFile(self.animation.getHDFFile())
        branch = self.dialog_dataselection.getBranch()

        if (branch != ""):
            self.animation.setAnimationBranch(branch)

    def generateAnimationData(self):
        #try:
        self.animation.initializeAnimation()
        self.animation.loadAnimation()
        #except:
        #    print "Exception"
    def plotAnimation(self):

        self.generateAnimationData()
        p = AnimationPlot(self.animation, self)
        p.plotAllDataCursor()
        p.canvas.draw()
        p.show()

    #----------------------------------------------------------
    #file select window
    #-------------------------------------------------------
    # def selectFile():
    #     lineEdit.setText(QFileDialog.getOpenFileName())
    #
    # pushButton.clicked.connect(selectFile)
    # #----------------------------------------------------------

    def exportHDFFile(self, path):

        hdf = tables.openFile(path, 'w')
        array = hdf.createArray("/", "animation", self.animation.signal.getAnimationData().tolist())
        #todo: make an array, time vector. self.animation.signal.getTimeVectorStuffSomewhere()
        hdf.close()
        
    #!!!
    def exportAnimation(self):

        folder_path = self.folder_path + "/data/outputs/"

        inputDialog = QtGui.QInputDialog()
        
        path, result = inputDialog.getText(self, "Export animation", "HDF file name to export the animation (i.e. animation1):")

        if (result):
            full_path = str(path) + ".hdf"
                
            if (os.path.isfile(folder_path + full_path)):
                question = QMessageBox.question(self, "File already exist", "This file already exists. Do you really want to continue this operation? All the information stored in the file will be lost!", QMessageBox.Yes | QMessageBox.No)

                if (question == QMessageBox.Yes):
                    self.generateAnimationData()
                    self.exportHDFFile(folder_path + full_path)
                else:
                    self.exportAnimation()
            else:
                self.generateAnimationData()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.exportHDFFile(folder_path + full_path)

    #play a test video
    def playTest(self):

        self.generateAnimationData()
        p = TestVid(self.animation, self)
        p.close()






    def selectAnimationAudio(self):

        audio_file = self.dialog_wavselection.getWAVFile()

        if (audio_file != ""):
            
            self.animation.setWAVFile(audio_file)
            self.text_audio.setText(audio_file)
        
    def selectAnimationSignal(self):
        
        signal_file = self.dialog_signalselection.getHDFFile()

        if (signal_file != ""):
            
            self.animation.setHDFFile(signal_file)
            self.text_signal.setText(signal_file)
            self.button_select_data.setEnabled(True)
        
    def changeAnimationName(self):

        name, result = QInputDialog.getText(self, "Animation name", "Name given to the animation:", text=self.animation.getName())

        name = str(name)
        
        if (result):
            if (name != ""):
                self.animation.setName(str(name))
                self.label_animation_name.setText(name)

            
    def saveAnimation(self):

        if (self.animation.getFile() == ""):
            
            folder_path = self.folder_path + "/data/animations/"

            inputDialog = QtGui.QInputDialog()
        
            path, result = inputDialog.getText(self, "Save animation", "HDF file name to save the animation (i.e. animation1):")

            if (result):
                full_path = str(path) + ".hdf"
                
                if (os.path.isfile(folder_path + full_path)):
                    question = QMessageBox.question(self, "File already exist", "This file already exists. Do you really want to continue this operation? All the information stored in the file will be lost!", QMessageBox.Yes | QMessageBox.No)

                    if (question == QMessageBox.Yes):
                        self.animation.setFile(full_path)
                        self.animation.saveFile()
                        self.label_animation_file.setText(full_path)
                        self.main_window.reloadAnimationsFromList()
                    else:
                        self.saveAnimation()
                else:
                    self.animation.setFile(full_path)
                    self.animation.saveFile()
                    self.label_animation_file.setText(full_path)
                    self.main_window.reloadAnimationsFromList()
        else:
            self.animation.saveFile()
            self.main_window.reloadAnimationsFromList()

    def setupVariablesTable(self):

        model = QStandardItemModel(self.table_variables)
        model.setHorizontalHeaderItem(0, QStandardItem(QString("Variable")))
        model.setHorizontalHeaderItem(1, QStandardItem(QString("Value")))

        self.table_model = model
        
        self.table_variables.setModel(model)

    def tableItemChanged(self, item):

        row = item.row()
        variable = str(self.table_model.item(row, 0).text())
        index = self.list_list.currentRow()
        parameter = self.animation.getOrderedList()[index]
        
        try:
            value = float(item.text())
        except:
            value = float(parameter.getVariable(variable))

        parameter.setVariable(variable, value)
        item.setText(str(value))

    def changedAnimationType(self):

        if (self.animation.isLoaded()):
            animation_type = ANIMATION_TYPE_HDF_FILE
            if (self.check_signal.isChecked()):
                animation_type = ANIMATION_TYPE_WAV_FILE
                
            self.animation.setAnimationType(animation_type)

            self.updateListControls()
        
    def updateListControls(self):

        if (self.animation.isLoaded()):

            self.label_animation_name.setText(self.animation.getName())
            self.label_animation_file.setText(self.animation.getFile())

            self.text_audio.setText(self.animation.getWAVFile())
            self.text_signal.setText(self.animation.getHDFFile())

            checked = False
            if (self.animation.getAnimationType() == ANIMATION_TYPE_WAV_FILE):
                checked = True

            self.text_signal.setEnabled(not checked)
            self.button_signal.setEnabled(not checked)

            if (not checked):
                if (self.animation.getHDFFile() != ""):
                    self.button_select_data.setEnabled(True)
                else:
                    self.button_select_data.setEnabled(False)
            else:
                self.button_select_data.setEnabled(False)        
            
            self.check_signal.setChecked(checked)
            
            self.updateParametersList()
            self.updateListToolbarStatus()
            
        else:
            
            self.label_animation_name.setText("-")
            self.label_animation_file.setText("-")

            self.text_audio.setText("")
            self.text_signal.setText("")
            


    def updateParametersList(self):

        selected = self.list_list.currentIndex()
        
        self.list_list.clear()
        
        if (self.animation.isLoaded()):
            for item in self.animation.getOrderedList():
                self.list_list.addItem(item.getName())

        self.list_list.setCurrentIndex(selected)

    def updateVariablesTable(self):

        index = self.list_list.currentRow()
        
        self.setupVariablesTable()

        if (self.animation.getOrderedList().size  >= (index + 1)):
            parameter = self.animation.getOrderedList()[index]
            i = 0

            if (isinstance(parameter, IInteractiveParameter)):
                self.button_interaction.setEnabled(True)
            else:
                self.button_interaction.setEnabled(False)
                
            for variable in parameter.getVariables():
                var = QStandardItem(QString(variable))
                var.setEditable(False)
                self.table_model.setItem(i, 0, var)
                self.table_model.setItem(i, 1, QStandardItem(QString(str(parameter.getVariable(variable)))))
                i+=1
            self.table_model.itemChanged.connect(self.tableItemChanged)    

    def updateListToolbarStatus(self):

        item = self.list_list.currentItem()
        
        if (self.animation.isLoaded()):
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)
        
        if (item is None):
            self.button_up.setEnabled(False)
            self.button_down.setEnabled(False)
            self.button_remove.setEnabled(False)

            return
        else:
            self.button_up.setEnabled(True)
            self.button_down.setEnabled(True)
            self.button_remove.setEnabled(True)


        index = self.list_list.currentRow()
        
        self.updateVariablesTable()
        
        if (index == self.list_list.count() - 1):
            self.button_down.setEnabled(False)

        if (index == 0):
            self.button_up.setEnabled(False)

            
    def moveListItem(self, down):

        item = self.list_list.currentItem()

        if (not(item is None)):
            index = self.list_list.currentRow()
            if (down):
                self.animation.moveDown(index)
            else:
                self.animation.moveUp(index)

            self.updateParametersList()
            self.updateListToolbarStatus()

            
    def moveListItemUp(self):
        
        next = max(0, self.list_list.currentRow() - 1)
        self.moveListItem(False)
        self.list_list.setCurrentRow(next)

        
    def moveListItemDown(self):
        
        next = min(self.list_list.count() - 1, self.list_list.currentRow() + 1)
        self.moveListItem(True)
        self.list_list.setCurrentRow(next)

    
    def addParameterToList(self):
        
        if (self.animation.isLoaded()):

            parameter_file = self.dialog_parameterselection.getParameterFile()
    
            if (parameter_file != ""):

                parameter = self.animation.getParameterFromFile(parameter_file.split('.')[0])
                self.animation.addParameter(parameter)
                
                self.updateListControls()

    def removeParameterFromList(self):

        if (self.animation.isLoaded()):
            order = self.list_list.currentRow()

            self.animation.removeParameterByOrder(order)

            if (self.animation.getOrder().size < (order + 1)):
                self.list_list.setCurrentRow(order - 1)

            self.updateListControls()


class AnimationPlot(QtGui.QDialog):

    def __init__(self, animation, parent=None):

        super(AnimationPlot, self).__init__(parent)
        
        self.animation = animation
        self.datanow = self.animation.signal.getAnimationData()
        self.datainput = self.animation.signal.getData()
        self.dataaudio = self.animation.wavsignal.getData()

        self.figure, self.axes = plt.subplots(3, figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.button_close = QtGui.QPushButton('Quit', parent=self)
        self.button_close.clicked.connect(self.close)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.button_close)

        self.multi = None
        
        self.setLayout(layout)
        self.setupXValues()

        
    def setupXValues(self):
        
        step = 1.0
        time = 1.0

        # calculates the x axis for both signals
        if (self.animation.getAnimationType() == ANIMATION_TYPE_WAV_FILE):
            time = self.animation.wavsignal.getTotalSeconds()
            step = 1.0 / self.animation.wavsignal.getFileRate()
        elif (self.animation.getAnimationType() == ANIMATION_TYPE_HDF_FILE):
            time = float(self.animation.signal.getData().size) / self.animation.signal.getFPS()
            step = 1.0 / self.animation.signal.getFPS()

            
        self.x_data_range = np.arange(0, time, step)
        self.x_animation_range = np.arange(0, time, time / self.datanow.size)
        self.x_audio_range = np.arange(0, self.animation.wavsignal.getTotalSeconds(), 1.0 / self.animation.wavsignal.getFileRate())

    def plotAllData(self):
        
        for i in range(0, len(self.axes)):
            self.axes[i].clear()
            
        plt_animation, = self.axes[0].plot(self.x_animation_range, self.datanow, color='r', label='Animation Data')
        self.axes[0].set_xlim([0, self.x_animation_range[-1]])
        self.axes[0].set_title("Animation Data (" + str(self.x_animation_range.size) + " samples)")
        
        plt_data, = self.axes[1].plot(self.x_data_range, self.datainput, label='Original Data')
        self.axes[1].set_xlim([0, self.x_data_range[-1]])
        self.axes[1].set_ylabel("Amplitude")
        self.axes[1].set_title("Original Data (" + str(self.x_data_range.size) + " samples)")
        
        plt_audio, = self.axes[2].plot(self.x_audio_range, self.dataaudio, label='Audio data', color='black')
        self.axes[2].set_xlim([0, self.x_audio_range[-1]])
        self.axes[2].set_xlabel("Time (s)")
        self.axes[2].set_title("Audio Data (" + str(self.x_audio_range.size) + " samples)")

        self.figure.subplots_adjust(0.11, 0.10, 0.96, 0.95, None, 0.30)

    def plotAllDataCursor(self):
        
        if (self.multi == None):
            self.multi = widgets.MultiCursor(self.canvas, self.axes)
        
        self.plotAllData()

class TestVid(QDialog):

    def __init__(self, animation, parent=None):

        super(TestVid, self).__init__(parent)

        self.animation = animation
        self.datanow = self.animation.signal.getAnimationData()
        self.datainput = self.animation.signal.getData()
        self.dataaudio = self.animation.wavsignal.getData()


        time = 1.0
        if (self.animation.getAnimationType() == ANIMATION_TYPE_WAV_FILE):
            time = self.animation.wavsignal.getTotalSeconds()

            fps = self.animation.wavsignal.getFileRate()

        elif (self.animation.getAnimationType() == ANIMATION_TYPE_HDF_FILE):
            time = float(self.animation.signal.getData().size) / self.animation.signal.getFPS()

            fps = self.animation.signal.getFPS()




        #Circle and Images
        surface = gizeh.Surface(width=1280, height=1040) # dimensions in pixel
        circle = gizeh.circle (r=40, # radius, in pixels
                               xy= [512, 512], # coordinates of the center
                               fill= (.5,.5,.5)) # 'red' in RGB coordinates
        circle.draw( surface ) # draw the circle on the surface
        surface.get_npimage() # export as a numpy array (we will use that)

        W,H = 1280, 1040 # width, height, in pixels

        duration = time # duration of the clip, in seconds
        self.x_animation_range = np.arange(0, time, time / self.datanow.size)
        x_animation_range = self.x_animation_range.tolist()
        datanow = self.datanow
        print x_animation_range
        def make_frame(t):
            surface = gizeh.Surface(W,H, bg_color=(1,1,1))
            radius = 60

            circle = gizeh.circle(radius, xy = (W/2, H/2+(datanow[x_animation_range.index(t)])*40), fill=(.5,.5,.5))
            circle.draw(surface)
            return surface.get_npimage()


        surface.write_to_png("my_drawing.png") # export as a PNG

        #AUDIOCLIP
        audio = AudioFileClip("/home/stan/Communication_Dynamics_Laboratory/mqueue/data/wav/%s" % self.animation.getWAVFile())



        #VIDEOCLIP
        clip = VideoClip(make_frame, duration=duration).set_audio(audio)


        #Export to Video
        clip.write_videofile('my_animation.mp4', fps=fps) # export as video

        #app = QtGui.QApplication(sys.argv)
        self.vp = Phonon.VideoPlayer(Phonon.VideoCategory)
        mobj = self.vp.mediaObject()

        self.vp.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.vp.show()
        media = Phonon.MediaSource('my_animation.mp4')
        self.vp.load(media)
        self.vp.play()
        self.vp.finished.connect(self.vp.deleteLater)
