# -*- coding: utf-8 -*-

from parameters import *

from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from scipy.stats import moment

VIAPOINTS_TYPE = 1007
DEFAULT_OFFSET = -1.0
ANIMATION_TYPE_NONE = 0
ANIMATION_TYPE_WAV_FILE = 1
ANIMATION_TYPE_HDF_FILE = 2

class Points():

    vp = np.array([])
    ts = np.array([])
    tau = np.array([])
    coef = np.array([])
    next = np.array([])

class ViaPointsParameter(IInteractiveParameter):

    def __init__(self):

        IParameter.__init__(self, "ViaPoints", VIAPOINTS_TYPE)
        
        self.setVariable("start_x", 0.0)
        self.setVariable("stop_x", 0.0)
        self.setVariable("via_points_moved", 0.0)
        self.setVariable("threshold", 0.01)

        self.vp = ViaPoints()
        
    def generateVariables(self, size):

        if (size < 0.0):
            size = 0
            
        size = int(size)
        v = range(0, size)
        variables = self.getVariables()
        
        self.setVariable("via_points_moved", size)

        #deletes extra variables
        for ind in variables:
            if str(ind).startswith('point_'):
                number = self._getPointPosition(ind)
                if (number > (size - 1)):
                    del(self._variables[ind])

        
        for i in v:
            var1 = 'point_x('+str(i)+')'
            var2 = 'point_y('+str(i)+')'
            
            if (not var1 in variables):
                self.setVariable(var1, 0.0)
                self.setVariable(var2, 0.0)

    def _getPointPosition(self, index):
        return int(str(index).replace('point_x(','').replace('point_y(','').replace(')', ''))

    def _getPointsMatrix(self):

        variables = self.getVariables()
        positions = np.zeros((self.getVariable('via_points_moved'), 2))
        
        for ind in variables:
            if (str(ind).startswith('point_x(')):
                pos = self._getPointPosition(ind)
                x = self.getVariable(ind)
                y = self.getVariable('point_y(' + str(pos) + ')')
                positions[pos, :] = np.asarray([x, y])

        return positions
    
    def applyParameter(self, data):

        start = int(self.getVariable('start_x'))
        stop = int(self.getVariable('stop_x'))

        if (start < stop):
            return data

        #creates new stack of data
        return_data = data.__copy__()
    
        new_data = np.vstack(data[start:stop+1])
        #generates via points for the region selected
        Xp, Xpd, Xpdd, Xpddd, vpts = self.vp.min_jerk_spline(new_data, 0.01, 1, 0)
        #gets the via points of the region
        points = vpts[0].vp[:, 0]

        #changes the via points for new values
        for x, y in self._getPointsMatrix():
            points[x] = y

        #generates new coeficients and recreates the data
        vpts[0].coef = self.vp.via_point_spline_coef(vpts)
        Xp, Xpd, Xpdd, Xpddd = self.vp.via_point_reconstruct(vpts)

        #inserts the new data to the original dataset
        return_data[start:stop+1] = np.hstack(Xp)
        
        return return_data

    def interaction(self, dataInput, dataNow, dataAudio, parent=None):
        p = InteractivePlot(self, dataInput, dataNow, dataAudio, parent)
        p.plotAllDataSpan()
        p.canvas.draw()
        p.show()


class InteractivePlot(QtGui.QDialog):

    def __init__(self, parameter, dataInput, dataNow, dataAudio, parent=None):

        super(InteractivePlot, self).__init__(parent)

        self.parameter = parameter
        self.datanow = dataNow
        self.datainput = dataInput
        self.dataaudio = dataAudio

        self.figure, self.axes = plt.subplots(3, figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.toolbar.addSeparator()
        self.button_via = QtGui.QPushButton('Select Via-Points Region')
        self.button_move = QtGui.QPushButton('Move points')
        self.button_move.setEnabled(False)
        
        self.button_via.clicked.connect(self.addSpanSelector)

        self.button_close = QtGui.QPushButton('Quit', parent=self)
        self.button_close.clicked.connect(self.close)

        self.button_clear = QtGui.QPushButton('Clear', parent=self)
        self.button_clear.clicked.connect(self.clearRegion)

        self.text_threshold = QtGui.QLineEdit(parent=self)
        self.text_threshold.setText(str(self.parameter.getVariable('threshold')))

        self.toolbar.addWidget(self.button_via)
        self.toolbar.addWidget(self.button_move)
        self.toolbar.addWidget(self.button_clear)
        
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.text_threshold)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.button_close)

        self.setLayout(layout)

        self.span, self.multi = None, None
        self.setupXValues()

            

    def clearRegion(self):
        self.parameter.setVariable('start_x', 0.0)
        self.parameter.setVariable('stop_x', 0.0)

        self.button_via.setText('Select Via-Points Region')
        
        self.plotAllDataSpan()
        self.canvas.draw()

    def zoomOut(self):

        self.axes[0].set_xlim([0, self.x_animation_range[-1]])
        self.canvas.draw()
        
    def addSpanSelector(self):

        self.span.visible = not self.span.visible
        if (self.span.visible):
            self.button_via.setText('End selecting Via-Points region')
        else:
            self.zoomOut()
            self.button_via.setText('Select Via-Points Region')
        
    def setupXValues(self):
        
        step = 1.0
        time = 1.0

        try:
            time = float(self.parameter.getHiddenVariable('SIGNAL_SIZE')) / self.parameter.getHiddenVariable('SIGNAL_RATE')
            step = 1.0 / self.parameter.getHiddenVariable('SIGNAL_RATE')
        except:
            pass


        self.x_data_range = np.arange(0, time, step)
        self.x_animation_range = np.arange(0, time, time / self.datanow.size)
        self.x_audio_range = np.arange(0, self.parameter.getHiddenVariable('AUDIO_TOTAL_SECONDS'), 1.0 / self.parameter.getHiddenVariable('AUDIO_FRAME_RATE'))

    def onSpanSelect(self, xmin, xmax):
        
        indmin, indmax = np.searchsorted(self.x_animation_range, (xmin, xmax))
        indmax = min(self.x_data_range.size-1, indmax)

        if ((indmax - indmin) <= 10):
            return
        
        self.parameter.setVariable('start_x', indmin)
        self.parameter.setVariable('stop_x', indmax)
        
        data = np.vstack(self.datanow)
        data = data[indmin:indmax, :]
        Xp, Xpd, Xpdd, Xpddd, vpts = self.parameter.vp.min_jerk_spline(data, 0.001, 1, 0)

        Xp_final = np.zeros(self.datanow.size)
        Xp_final[0:indmin] = np.NaN
        Xp_final[indmax:] = np.NaN
        
        Xp_final[indmin:indmax] = np.hstack(Xp[:,0])
        
        via_x = np.append(vpts[0].ts, data.size-1)
        via_x = via_x + indmin
        via_x = self.x_animation_range[via_x]
        
        self.axes[0].clear()

        lower = max(indmin - 10, 0)
        upper = min(indmax + 10, self.x_animation_range.size-1)

        plt_animation, = self.axes[0].plot(self.x_animation_range, self.datanow, color='r', label='Animation Data')
        self.axes[0].set_xlim([self.x_animation_range[lower], self.x_animation_range[upper]])
        
        self.axes[0].set_title("Animation Data (" + str(self.x_animation_range.size) + " samples)")
        
        self.axes[0].plot(self.x_animation_range, Xp_final, 'b-.', via_x, vpts[0].vp[:,0], 'go')
        mm = self.axes[0].get_ylim()
        
        self.axes[0].plot((via_x[0], via_x[0]), (mm[0], mm[1]), 'b-.')
        self.axes[0].plot((via_x[-1], via_x[-1]), (mm[0], mm[1]), 'b-.')

        self.axes[0].set_ylim(mm)
            
        self.canvas.draw()
        
        
    def plotAllDataSpan(self):
        
        if (self.span == None):
            self.span = widgets.SpanSelector(self.axes[0], self.onSpanSelect, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'), span_stays=True)

        if (self.multi == None):
            self.multi = widgets.MultiCursor(self.canvas, self.axes)
            
        self.span.visible = False
        
        self.plotAllData()                    
                            
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

        if (self.parameter.getVariable('start_x') != self.parameter.getVariable('stop_x')):
            self.onSpanSelect(self.x_data_range[self.parameter.getVariable('start_x')],
                              self.x_data_range[self.parameter.getVariable('stop_x')])
        self.zoomOut()

class ViaPoints():

    def plotData(self, vpts, X):

        try:
            n_data, n_traj = X.shape
        except:
            n_data = 1
            n_traj = X.size

            
        T = range(0, n_data)
        Xp, Xpd, Xpdd, Xpddd = self.via_point_reconstruct(vpts)

        fig, axes = plt.subplots(n_traj)
        if (n_traj == 1):
            axes.plot(T, X[:,0], 'y-', T, Xp[:,0], 'b-.', np.append(vpts[0].ts, n_data-1), vpts[0].vp[:,0], 'go')
                
        else:
            for i in range(0, n_traj):
                axes[i].plot(T, X[:,i], 'y-', T, Xp[:,i], 'b-.', np.append(vpts[i].ts, n_data-1), vpts[i].vp[:,0], 'go')

        plt.plot()

        return fig, axes
        
    def min_jerk_spline(self, X, threshold, kind=1, draw=0):

        if (isinstance(X, list)):
            X = np.array(X, dtype=float)

        if (not isinstance(X, np.ndarray)):
            return None

        n_sp = 1

        try:
            n_data, n_traj = X.shape
        except:
            n_data = 1
            n_traj = X.size
        
        vpts = np.array([], dtype=type(Points))
        #vpts = np.resize(vpts, (1, n_traj))
        
        for i in range(0, n_traj):
            pt = Points()
            pt.vp = np.asarray([[X[0, i], 0, 0], [X[n_data-1, i], 0, 0]], dtype=float)
            pt.ts = np.asarray([[0]])
            pt.tau = np.asarray([[n_data-1]])
            pt.coef = np.zeros(6, dtype=float)
            pt.coef = self.via_point_spline_coef(pt)
            vpts = np.append(vpts, pt)

        
        Xp,Xpd,Xpdd,Xpddd = self.via_point_reconstruct(vpts)
        
        bMSE = moment(X,2)
        res = X - Xp

        if (kind == 1):
            nMSE = moment(res,2) / bMSE
            mnMSE = np.mean(nMSE)
            crit = mnMSE
        elif (kind == 2):
            MSE = moment(res,2)
            mMSE = np.mean(MSE)
            crit = mMSE
        else:
            crit = np.sqrt(np.sum(np.power(res, 2), 2)).max()

                        
        while(crit > threshold):
            
            if (n_traj > 1):
                mat = np.sum(np.power(res, 2), axis=1)
                v, j = np.max(mat), np.argmax(mat)
            else:
                mat = np.power(res, 2)
                v, j = np.max(mat), np.argmax(mat)

            
            for n in range(n_sp-1, -1, -1):
                if ((vpts[0].ts[n] < j) and (vpts[0].ts[n]+vpts[0].tau[n] > j)):
                    break
            
            tau1 = j - vpts[0].ts[n]
            tau2 = vpts[0].ts[n] + vpts[0].tau[n] - j
            
            if ((tau1 < 1) or (tau2 < 1)):
                break
            
            for r in range(0, n_traj):
                
                vpts[r].vp = np.vstack([vpts[r].vp[0:n+1], [X[j, r], 0, 0], vpts[r].vp[n+1:n_sp+2]])
                vpts[r].ts = np.vstack([vpts[r].ts[0:n+1], [j], vpts[r].ts[n+1:n_sp+1]])
                vpts[r].tau = np.vstack([vpts[r].tau[0:n], [tau1], [tau2], vpts[r].tau[n+1:n_sp+1]])
                vpts[r].vp[:, 1], vpts[r].vp[:, 2] = self.optimal_via_points(vpts[r].vp[:, 0], vpts[r].tau)

                vpts[r].coef = self.via_point_spline_coef(vpts[r])

            n_sp = n_sp + 1

            Xp, Xpd, Xpdd, Xpddd = self.via_point_reconstruct(vpts)


            res = X - Xp

            if (kind == 1):
                nMSE = moment(res,2) / bMSE
                mnMSE = np.mean(nMSE)
                crit = mnMSE
            elif (kind == 2):
                MSE = moment(res,2)
                mMSE = np.mean(MSE)
                crit = mMSE
            else:
                crit = np.sqrt(np.sum(np.power(res, 2), 2)).max()

            
            if (draw):
                pass

        Xp, Xpd, Xpdd, Xpddd = self.via_point_reconstruct(vpts)
        
        if (draw):
            self.plotData(vpts, X)


        return (Xp, Xpd, Xpdd, Xpddd, vpts)
                

    def via_point_spline_coef(self, vpts):

        n_sp = vpts.tau.size
        coef = np.zeros((n_sp, 6))
        
        for i in range(0, n_sp):
            v = np.vstack(np.hstack([vpts.vp[i, :], vpts.vp[i+1, :]]))

            tau = vpts.tau[i]
            A = np.matrix([[1, 0, 0, 0, 0, 0], \
                          [0, 1, 0, 0, 0, 0], \
                          [0, 0, 0.5, 0, 0, 0], \
                          np.divide([-20, -12*tau, -3*tau**2, 20, -8*tau, tau**2], 2*tau**3, dtype=float),
                          np.divide([30, 16*tau, 3*tau**2, -30, 14*tau, -2*tau**2], 2*tau**4, dtype=float),
                          np.divide([-12, -6*tau, -1*tau**2, 12, -6*tau, tau**2], 2*tau**5, dtype=float)],\
                         dtype=float)

            val = np.dot(A, v).transpose()
            coef[i] = val

        return coef

    def optimal_via_points(self, pos, T):

        n_spline = T.size
        n_via = pos.size

        A = np.zeros((2*n_via, 2*n_via))
        B = np.zeros((n_via, 2*n_via))

        
        A[0, 0] = 384.0 / T[0]**3
        A[0, 1] = 336.0 / T[0]**3
        A[0, n_via] = 72.0 / T[0]**2
        A[0, n_via+1] = -48.0 / T[0]**2
        
        A[n_via-1, n_via-2] = 336.0 / T[n_spline-1]**3
        A[n_via-1, n_via-1] = 384.0 / T[n_spline-1]**3
        A[n_via-1, 2*n_via-2] = 48.0 / T[n_spline-1]**2
        A[n_via-1, 2*n_via-1] = -72.0 / T[n_spline-1]**2

        A[n_via, 0] = 72.0 / T[0]**2
        A[n_via, 1] = 48.0 / T[0]**2
        A[n_via, n_via] = 18.0 / T[0]
        A[n_via, n_via+1] = -6.0 / T[0]

        A[2*n_via - 1, n_via-2] = -48.0 / T[n_spline-1]**2
        A[2*n_via - 1, n_via-1] = -72.0 / T[n_spline-1]**2
        A[2*n_via - 1, 2*n_via-2] = -6.0 / T[n_spline-1]
        A[2*n_via - 1, 2*n_via-1] = 18.0 / T[n_spline-1]
        
        for i in range(1, n_via - 1):
            
            A[i, i-1] = 336.0 / T[i-1]**3
            A[i, i] = 384.0 / T[i-1]**3 + 384.0 / T[i]**3
            A[i, i+1] = 336.0 / T[i]**3

            A[i, n_via+i-1]   = 48.0 / T[i-1]**2
            A[i, n_via+i] = -72.0 / T[i-1]**2 + 72.0 / T[i]**2
            A[i, n_via+i+1] = -48.0 / T[i]**2
            
            A[n_via+i, i-1]   = -48.0 / T[i-1]**2
            A[n_via+i, i] = -72.0 / T[i-1]**2 + 72.0 / T[i]**2
            A[n_via+i, i+1] =  48.0 / T[i]**2
            
            A[n_via+i, n_via+i-1]   = -6.0 / T[i-1]
            A[n_via+i, n_via+i] = 18.0 / T[i-1] + 18.0 / T[i]
            A[n_via+i, n_via+i+1] = -6.0 / T[i]

        
        B[0, 0] = 720.0 / T[0]**4
        B[0, 1] = 720.0 / T[0]**4
        B[0, n_via] = 120.0 / T[0]**3
        B[0, n_via+1] = -120.0 / T[0]**3

        B[n_via-1, n_via-2] = -720.0 / T[n_spline-1]**4
        B[n_via-1, n_via-1] = -720.0 / T[n_spline-1]**4
        B[n_via-1, 2*n_via-2] = -120.0 / T[n_spline-1]**3
        B[n_via-1, 2*n_via-1] = 120.0 / T[n_spline-1]**3

        for i in range(1, n_via - 1):
            
            B[i, i-1] = -720.0 / T[i-1]**4
            B[i, i] = -720.0 / T[i-1]**4 + 720.0 / T[i]**4
            B[i, i+1] = 720.0 / T[i]**4

            B[i, n_via+i-1]   = -120.0 / T[i-1]**3
            B[i, n_via+i] = 120.0 / T[i-1]**3 + 120.0 / T[i]**3
            B[i, n_via+i+1] = -120.0 / T[i]**3

        B = B.transpose()
        res = np.dot((-1 * np.linalg.inv(A)), np.dot(B, pos))

        vel = res[0:n_via]
        acc = res[n_via:2*n_via+1]

        return (vel, acc)

    def normalize(self, vector):

        val = max(abs(vector.max()), abs(vector.min()))

        if (val == 0.0 or val == np.nan):
            return vector

        return vector / val
    
    def via_point_reconstruct(self, vpts):
        
        n_traj = vpts.size
        n_sp = vpts[0].tau.size
    
        n_data = vpts[0].tau[n_sp-1] + vpts[0].ts[n_sp-1]
        
        Xp = np.zeros((n_data+1, n_traj))
        Xpd = np.zeros((n_data+1, n_traj))
        Xpdd = np.zeros((n_data+1, n_traj))
        Xpddd = np.zeros((n_data+1, n_traj))


        for j in range(0, n_sp):
            n = vpts[0].ts[j]
            t = np.arange(0, vpts[0].tau[j]+1)

            C = np.vstack(vpts[0].coef[j])

            for i in range(1, n_traj):
                C = np.append(C, np.vstack(vpts[i].coef[j]), 1)

            index = n+vpts[0].tau[j]+1
            T = np.array([np.ones(t.size), t, np.power(t, 2), np.power(t, 3), np.power(t, 4), np.power(t, 5)]).transpose()


            Xp[n:index] = np.dot(T, C)
            T = np.array([np.ones(t.size), 2*t, 3*np.power(t, 2), 4*np.power(t, 3), 5*np.power(t, 4)]).transpose()

            Xpd[n:index] = np.dot(T, C[1:6])

            T = np.array([2*np.ones(t.size), 6*t, 12*np.power(t, 2), 20*np.power(t, 3)]).transpose()
            Xpdd[n:index] = np.dot(T, C[2:6])

            T = np.array([6*np.ones(t.size), 24*t, 60*np.power(t, 2)]).transpose()
            Xpddd[n:index] = np.dot(T, C[3:6])


        return (np.vstack(Xp), np.vstack(Xpd), np.vstack(Xpdd), np.vstack(Xpddd))


    def move_via_point(self, X, vpts, index, to_x, to_y):
        vpts[0].vp[index, 0] = to_y
        vpts[0].ts[index] = to_x
        vpts[0].tau[index-1] = vpts[0].ts[index] - vpts[0].ts[index-1]
        vpts[0].tau[index] = vpts[0].ts[index+1] - vpts[0].ts[index]

        vpts[0].vp[:, 1], vpts[0].vp[:, 2] = self.optimal_via_points(vpts[0].vp[:, 0], vpts[0].tau)
        vpts[0].coef = self.via_point_spline_coef(vpts[0])

        return self.via_point_reconstruct(vpts) +  (vpts,)

def loadParameter():

    return ViaPointsParameter()
