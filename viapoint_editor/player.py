# -*- coding: utf-8 -*-

## local imports

from window import *

global window, app

def windowStart():
    
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('ui/gfx/Iconsmind-Outline-Double-Circle.ico'))
    window = MainWindow()
    
    window.show()

    return (app, window)

def startApp():
    
    global app, window, threads
    
    app, window = windowStart()
    
    app.exec_()

    sys.exit()


startApp()



