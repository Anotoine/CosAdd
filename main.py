#####################################################################################
#                                                                                   #
#                PLOT A LIVE GRAPH IN A PYQT WINDOW                                 #
#                EXAMPLE 2                                                          #
#               ------------------------------------                                #
# This code is inspired on:                                                         #
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/speeding-up-the-plot-animation  #
#                                                                                   #
#####################################################################################

from __future__ import annotations
from typing import *
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import random

class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''
    def __init__(self):
        super().__init__()
        # 1. Window settings
        self.setGeometry(50, 50, 1700, 1000)
        self.setWindowTitle("Matplotlib live plot in PyQt")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QGridLayout()
        self.lyt.setSpacing(10)
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        # placing some UI elements
        self.PushButton = QtWidgets.QPushButton(self)
        self.PushButton.setText("Prueba")
        self.lyt.addWidget(self.PushButton, 0, 0)

        self.CheckBox = QtWidgets.QCheckBox(self)
        self.CheckBox.setCheckState(QtCore.Qt.Checked)
        self.lyt.addWidget(self.CheckBox, 1, 0)

        self.ComboBox = QtWidgets.QComboBox(self)
        self.ComboBox.addItems(["One", "Two", "Three"])
        self.lyt.addWidget(self.ComboBox, 2, 0)

        self.Label = QtWidgets.QLabel(self)
        self.Label.setText("Prueba")
        self.lyt.addWidget(self.Label, 3, 0)
        
        self.Slider = QtWidgets.QSlider(self)
        self.Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.lyt.addWidget(self.Slider, 4, 0)

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_range=[-5, 6], y_range=[-10, 10], interval=100)
        self.lyt.addWidget(self.myFig, 0, 1, 10, 1)

        # 3. Show
        self.show()
        return

class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_range:List, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_range
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(x_range[0]*10, x_range[1]*10))
        y = list([0]*len(x))

        # Store a figure and ax
        self.ax = self.figure.subplots()
        self.ax.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])

        plotcols = ["black","red", "orange", "yellow", "green"]

        self.lines = []
        for i in range(len(plotcols)):
            self.lines.append(self.ax.plot(x,y, lw=2, color=plotcols[i])[0])

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, init_func=None, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        y = get_data()
        for i, line in enumerate(self.lines):
            line.set_ydata(y[i])

        return self.lines


# Data source
# ------------

Waves = []
for i in range(0,4):
    Waves.append({"show"        : True,
                  "amplitude"   : 1.0,
                  "frequency"   : 10.0,
                  "lambda"      : 10.0,
                  "phi"         : 0.0})
Waves[0]["frequency"] = 1.0
Waves[1]["frequency"] = 2.0
Waves[2]["frequency"] = 4.0
Waves[3]["frequency"] = 10.0

t = 0
def get_data():
    global t
    t += 1

    z = np.linspace(-5, 5, 110)
    vals = []
    #Computing suma
    for w in Waves:
        k = 2*np.pi/w["lambda"]
        omega = 2*np.pi*w["frequency"]
        vals.append(w["amplitude"] * np.cos(k*z-omega*t/1000))

    vals.append(np.sum(vals, axis=0))
    return vals

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    qapp.exec_()