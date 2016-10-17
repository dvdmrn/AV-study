from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog
import sub.printfriend

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.button = QtGui.QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        print ('Hello World')
        sub.printfriend.printPoo()
        

    def selectFile(self):
        self.fileDialog = QtGui.QFileDialog(self)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())