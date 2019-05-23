

global SOUND
from warnings import warn
import sys

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    # string = ((
    #     "Module 'matplotlib' is not installed. To enable the quick preview "
    #     "feature of csdfpy module, install 'matplotlib' using "
    #     "'pip install matplotlib'."
    #     )
    # )
    print(str(e))
    sys.exit()

import numpy as np
import matplotlib
try:
    SOUND = 1
    import sounddevice as sd
except:
    SOUND = 0
    string = ((
        "Module 'sounddevice' is not installed. All audio data files will not be "
        "played. To enable audio files, install 'sounddevice' using "
        "'pip install sounddevice'."
        )
    )
    warn(string)

import sys
import time
try:
    from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
    if is_pyqt5():
        from matplotlib.backends.backend_qt5agg import (
            FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
    else:
        from matplotlib.backends.backend_qt4agg import (
            FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
    from matplotlib.figure import Figure
except:
    pass


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


def quick_preview(data):
    if matplotlib.get_backend() in ['Qt5Agg', 'QT4Agg']:
        # print(f"using {matplotlib.get_backend()} backend.")
        qapp = QtWidgets.QApplication(sys.argv)
        app = ApplicationWindow(data)
        app.show()
        sys.exit(qapp.exec_())
    else:
        quick_display(data)

def quick_display(data):
    x = data.independent_variables
    y = data.dependent_variables
    y_len = len(y)
    y_grid = int(y_len/2) + 1

    if len(x) <= 2:
        if y_len <= 2:
            fig, ax = plt.subplots(y_grid)
            if y_len == 1:
                ax = [[ax]]
            else:
                ax = [ax]
        else:
            fig, ax = plt.subplots(y_grid, 2)

        fig.canvas.set_window_title(data.filename)

    if len(x) == 1:
        for i in range(y_len):
            if y[i].quantity_type == 'scalar':
                plot1D(x, y, i, ax)
            if 'vector' in y[i].quantity_type:
                vector_plot(x, y, i, fig, ax)
            if 'audio' in y[i].quantity_type:
                audio(x, y, i, fig, ax)

        plt.tight_layout(w_pad=0.0, h_pad=0.0)
        plt.show()

    if len(x) == 2:
        for i in range(y_len):
            if y[i].quantity_type in ['RGB', 'RGBA']:
                RGB(x, y, i, fig, ax)
            if y[i].quantity_type in ['scalar']:
                twoD_scalar(x, y, i, fig, ax)
            if 'vector' in y[i].quantity_type:
                vector_plot(x, y, i, fig, ax)

        plt.tight_layout(w_pad=0.0, h_pad=0.0)
        plt.show()

## ========================================================= ##

def plot1D(x, y, i0, ax):
    i = int(i0/2); j= int(i0%2)
    components = y[i0].components.shape[0]
    for k in range(components):
        ax[i][j].plot(x[0].coordinates, y[i0].components[k].real)
        if 'complex' in y[i0].numeric_type:
            ax[i][j].plot(x[0].coordinates, y[i0].components[k].imag)

        ax[i][j].set_xlim(x[0].coordinates[0].value, x[0].coordinates[-1].value)
        ax[i][j].set_xlabel(x[0].axis_label)
        ax[i][j].set_ylabel(y[i0].axis_label[0])
        ax[i][j].set_title(f"{y[i0].name}")
        ax[i][j].grid(color='gray', linestyle='--', linewidth=0.5)

def RGB(x, y, i0, fig, ax):
    i = int(i0/2); j=i0%2
    y0 = y[i0].components
    ax[i][j].imshow(np.moveaxis(y0/y0.max(), 0, -1 ))
    ax[i][j].set_title(f"{y[i0].name}")

def twoD_scalar(x, y, i0, fig, ax):
    i = int(i0/2); j=i0%2

    extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
              x[1].coordinates[0].value, x[1].coordinates[-1].value]
    cs = ax[i][j].imshow(y[i0].components[0].astype(np.float64), extent=extent,
                    origin='lower', aspect='auto',
                    cmap='Blues')
    cbar = fig.colorbar(cs, ax=ax[i][j])
    cbar.ax.minorticks_off()
    cbar.ax.set_ylabel(y[i0].axis_label[0], rotation=270)
    ax[i][j].set_xlabel(x[0].axis_label)
    ax[i][j].set_ylabel(x[1].axis_label)
    ax[i][j].set_title(f"{y[i0].name}")
    ax[i][j].grid(color='gray', linestyle='--', linewidth=0.5)

def vector_plot(x, y, i0, fig, ax):
    i = int(i0/2); j=i0%2
    x0 = x[0].coordinates.value
    if len(x) == 2:
        x1 = x[1].coordinates.value
    else:
        x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y[i0].components[0]
    v1 = y[i0].components[1]
    ax[i][j].quiver(x0, x1, u1, v1,  pivot='middle')
    ax[i][j].set_xlabel(x[0].axis_label)
    ax[i][j].set_xlim(x[0].coordinates[0].value, x[0].coordinates[-1].value)
    if len(x) == 2:
        ax[i][j].set_ylim(x[1].coordinates[0].value, x[1].coordinates[-1].value)
        ax[i][j].set_ylabel(x[1].axis_label)
    else:
        ax[i][j].set_ylim([-y.components.max(),y.components.max()])
    ax[i][j].set_title(f"{y[i0].name}")
    ax[i][j].grid(color='gray', linestyle='--', linewidth=0.5)

def audio(x, y, i0, fig, ax):
    plot1D(x, y, i0, ax)
    if SOUND == 1:
        data_max = y[i0].components.max()
        sd.play(0.9*y[i0].components.T/data_max, 1/x[0].increment.to('s').value)





## ========================================================= ##


def plot_line(x, y, ax):
    components = y.components.shape[0]
    for k in range(components):
        ax.plot(x[0].coordinates, y.components[k].T.real)
        if 'complex' in y.numeric_type:
            ax.plot(x[0].coordinates, y.components[k].T.imag)

        if x[0].dimension_type != 'labeled':
            ax.set_xlim(x[0].coordinates[0].value, x[0].coordinates[-1].value)

        ax.set_xlabel(x[0].axis_label)
        ax.set_ylabel(y.axis_label[0])
        ax.set_title(f"{y.name}")
        ax.grid(color='gray', linestyle='-', linewidth=0.5)

def plot_image(x, y, fig, ax):
    if x[0].dimension_type != 'labeled':
        extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
                x[1].coordinates[0].value, x[1].coordinates[-1].value]
                
    cs = ax.imshow(y.components[0].real.astype(np.float64), extent=extent,
                   origin='lower', aspect='auto', cmap='viridis', interpolation='none')
    cbar = fig.colorbar(cs, ax=ax)
    cbar.ax.minorticks_off()
    cbar.set_label(y.axis_label[0])
#     cbar.ax.set_ylabel(y.axis_label[0], rotation=270, labelpad=+5)
    ax.set_xlabel(x[0].axis_label)
    ax.set_ylabel(x[1].axis_label)
    ax.set_title(f"{y.name}")
    ax.grid(color='gray', linestyle='--', linewidth=0.1)

def plot_vector(x, y, ax):
#     i = int(i0/2); j=i0%2
    if x[0].dimension_type != 'labeled':
        x0 = x[0].coordinates.value
        if len(x) == 2:
            x1 = x[1].coordinates.value
        else:
            x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y.components[0]
    v1 = y.components[1]
    ax.quiver(x0, x1, u1, v1, pivot='middle')
    ax.set_xlabel(x[0].axis_label)
    ax.set_xlim(x[0].coordinates[0].value, x[0].coordinates[-1].value)
    if len(x) == 2:
        ax.set_ylim(x[1].coordinates[0].value, x[1].coordinates[-1].value)
        ax.set_ylabel(x[1].axis_label)
    else:
        ax.set_ylim([-y.components.max(),y.components.max()])
    ax.set_title(f"{y.name}")
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

def plot_RGB(x, y, ax):
    y0 = y.components
    ax.imshow(np.moveaxis(y0/y0.max(), 0, -1 ))
    ax.set_title(f"{y.name}")

def plot_audio(x, y, ax):
    plot_line(x, y, ax)
    # print (SOUND)
    if SOUND == 1:
        data_max = y.components.max()
        sd.play(0.9*y.components.T/data_max, 1/x[0].increment.to('s').value)
    
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, dictionary):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self._main.setWindowTitle(dictionary.filename)
        self.setCentralWidget(self._main)
        tabs = QtWidgets.QTabWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        # def display(event_location):
        #     print('x={0}, y={1}, xdata={2}, ydata={3}'.format( \
        #         event_location.x, event_location.y,
        #         event_location.xdata, event_location.ydata))

        
        def set_gui():
            tab_ = QtWidgets.QWidget()
            layout_ = QtWidgets.QVBoxLayout(tab_)
            layout_.setSpacing(0)
            layout_.setContentsMargins(0,0,0,0)
            canvas = FigureCanvas(Figure(tight_layout=True)) # figsize=(5, 3),
            layout_.addWidget(canvas)
            layout_.addWidget(NavigationToolbar(canvas, self))
            tabs.addTab(tab_, f'Dependent variable {i}')
            
            ax = canvas.figure.subplots()
            fig = canvas.figure
            return fig, ax

        number_of_dependents = len(dictionary.dependent_variables)
        number_of_independents = len(dictionary.independent_variables)
        # tab_ = []
        # layout_ = []
        
        for i in range(number_of_dependents):
            # tab_.append(QtWidgets.QWidget())
            # layout_.append(QtWidgets.QVBoxLayout(tab_[-1]))
            # layout_[-1].setSpacing(0)
            # layout_[-1].setContentsMargins(0,0,0,0)
            # canvas = FigureCanvas(Figure(tight_layout=True)) # figsize=(5, 3),
            # layout_[-1].addWidget(canvas)
            # layout_[-1].addWidget(NavigationToolbar(canvas, self))
            # tabs.addTab(tab_[-1], f'Dependent variable {i}')
            
            # ax = canvas.figure.subplots()
            # fig = canvas.figure
            # cid = canvas.mpl_connect('axes_enter_event', display)

            x = dictionary.independent_variables
            y = dictionary.dependent_variables[i]


            # for j in range(number_of_independents):
            #     if x[j].FFT_output_order:
            #         x[j].FFT_output_order = False

            if (number_of_independents == 1):
                
                if y.quantity_type == 'scalar':
                    fig, ax = set_gui()
                    plot_line(x, y, ax)
                if 'audio' in y.quantity_type:
                    fig, ax = set_gui()
                    plot_audio(x, y, ax)
                if y.quantity_type == 'vector_2':
                    fig, ax = set_gui()
                    plot_vector(x, y, ax)
                    
            if (number_of_independents == 2):
                # x = dictionary.independent_variables
                # y = dictionary.dependent_variables[i]
                if y.quantity_type == 'scalar':
                    fig, ax = set_gui()
                    if np.any([x[i].dimension_type=='labeled' for i in [0,1]]):
                        plot_line(x, y, ax)
                    else:
                        plot_image(x, y, fig, ax)
                if y.quantity_type == 'vector_2':
                    fig, ax = set_gui()
                    plot_vector(x, y, ax)
                if y.quantity_type in ['RGB', 'RGBA']:
                    fig, ax = set_gui()
                    plot_RGB(x, y, ax)

            
                
        layout.addWidget(tabs)

