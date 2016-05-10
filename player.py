# -*- coding: utf-8 -*-

## local imports

from window import *

global window, app

def windowStart():
    
    app = QtGui.QApplication(sys.argv)    
    window = MainWindow()
    
    window.show()

    return (app, window)

def startApp():
    
    global app, window, threads
    
    app, window = windowStart()
    
    app.exec_()

    sys.exit()


startApp()



