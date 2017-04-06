import sys
import os
from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtGui
from PyQt4.QtGui import *



class AnimationPlayerConsole(QtGui.QWidget):
    
    def __init__(self):
        super(AnimationPlayerConsole, self).__init__()
        self.initUI()
        
        
    def initUI(self):
        # self.setGeometry(600, 300, 400, 200)
        # self.setWindowTitle('Single Browse')     
        
        # btn = QtGui.QPushButton('Browse\n(SINGLE)', self)
        # btn.resize(btn.sizeHint())
        # btn.clicked.connect(self.SingleBrowse)
        # btn.move(150, 100)     
		self.w = QWidget()
		self.setWindowTitle('Compile animation')
		# Set window size.
		self.resize(450, 150)
		#----- Create hdf input -------------------------------\\
		self.hdfTextbox = QLineEdit(self)
		self.hdfTextbox.move(20, 20)
		self.hdfTextbox.resize(280,30)
		 

		 
		# Create a button in the window
		self.hdfButton = QPushButton('Select HDF file', self)
		self.hdfButton.move(320,20)
	

		# connect the signals to the slots
		self.hdfButton.clicked.connect(self.browseHdfFile)

		#-----------------------------------------------------//



		#----- Create wav input ------------------------------\\

		self.wavTextbox = QLineEdit(self)
		self.wavTextbox.move(20,60)
		self.wavTextbox.resize(280,30)

		self.wavButton = QPushButton('select WAV file', self)
		self.wavButton.move(320,60)

		# connect the signals to the slots
		self.wavButton.clicked.connect(self.browseWavFile)
		#-----------------------------------------------------//

		#----- construct animation ------------------------------\\

		self.createAnimationButton = QPushButton('create animation', self)
		self.createAnimationButton.move(20,100)
		self.createAnimationButton.clicked.connect(self.createAnimation)
		#haha cool all good now to show everything
		self.show()

		# app.exec_()

    def browseHdfFile(self):
        self.filePath = QtGui.QFileDialog.getOpenFileName(self, 
                                                       'Single File',
                                                       "~/Desktop",
                                                      '*.hdf')
        print('filePath',self.filePath, '\n')
        
        self.fileHandle = open(self.filePath, 'r')
        # self.lines = fileHandle.readlines()
        # for line in lines:
        #     print(line)
        self.hdfTextbox.setText(str(self.filePath))

    def browseWavFile(self):
        self.filePath = QtGui.QFileDialog.getOpenFileName(self, 
                                                       'Single File',
                                                       "~/Desktop",
                                                      '*.wav')
        print('filePath',self.filePath, '\n')
        
        self.fileHandle = open(self.filePath, 'r')
        # self.lines = fileHandle.readlines()
        # for line in lines:
        #     print(line)
        self.wavTextbox.setText(str(self.filePath))

    def createAnimation(self):
    	print("editiaksdfsakldfjdaslkfjsdaklfjsdlkfjsk")
        hdfFilePath = unicode(self.hdfTextbox.text().toUtf8(), encoding="UTF-8")
        wavFilePath = unicode(self.wavTextbox.text().toUtf8(), encoding="UTF-8")
        os.system("python animationplayer/HDFdrivenBallAnimation.py "+hdfFilePath+" "+wavFilePath)
    	
    
def main():
    app = QtGui.QApplication(sys.argv)
    w = AnimationPlayerConsole()
    # w.show()
    app.exec_()



if __name__ == '__main__':
    main()






#---------------------------------------------------
# # create our window
# app = QApplication(sys.argv)
# w = QWidget()
# w.setWindowTitle('Compile animation')
 
# # Create hdfTextbox
# hdfTextbox = QLineEdit(w)
# hdfTextbox.move(20, 20)
# hdfTextbox.resize(280,40)
 
# # Set window size.
# w.resize(320, 150)
 
# # Create a button in the window
# button = QPushButton('Select HDF file', w)
# button.move(20,80)
# # btn.clicked.connect(SingleBrowse)
 
# # Create the actions
# @pyqtSlot()
# def on_click():
# 	filePath = QtGui.QFileDialog.getOpenFileName(self,
#                                                        'Single File',
#                                                        "~/Desktop",
#                                                       '*.hdf')
# 	print('filePath',filePath, '\n')
# 	fileHandle = open(filePath, 'r')
# 	lines = fileHandle.readlines()
# 	for line in lines:
# 		print(line)
	

        

