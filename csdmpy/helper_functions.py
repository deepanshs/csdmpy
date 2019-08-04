# -*- coding: utf-8 -*-
"""Helper functions."""
import sys
from copy import deepcopy
from warnings import warn

from numpy.fft import fftshift

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.image import NonUniformImage
except ImportError as e:
    print(str(e))
    sys.exit()

import numpy as np

global SOUND
scalar = ["scalar", "vector_1", "pixel_1", "matrix_1_1", "symmetric_matrix_1"]

try:
    from matplotlib.backends.qt_compat import QtWidgets, is_pyqt5

    if is_pyqt5():
        from matplotlib.backends.backend_qt5agg import (
            FigureCanvas,
            NavigationToolbar2QT as NavigationToolbar,
        )
    else:
        from matplotlib.backends.backend_qt4agg import (
            FigureCanvas,
            NavigationToolbar2QT as NavigationToolbar,
        )
    from matplotlib.figure import Figure
except ImportError:
    pass


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


def preview(data_object):
    """Quick preview od the dataset."""
    axes = []
    data = deepcopy(data_object)
    # for i, dim in enumerate(data.dimensions):
    #     if hasattr(dim, "complex_fft"):
    #         if dim.complex_fft:
    #             npts = dim.count
    #             if npts % 2 == 0:
    #                 temp = npts * dim.increment / 2.0
    #             else:
    #                 temp = (npts - 1) * dim.increment / 2.0
    #             dim.coordinates_offset = dim.coordinates_offset - temp

    #             axes.append(-i - 1)
    #             dim.complex_fft = False

    for var in data.dependent_variables:
        var.components = fftshift(var.components, axes=axes)

    # print(matplotlib.get_backend())

    if matplotlib.get_backend() in ["Qt5Agg", "Qt4Agg"]:
        x = data.dimensions
        number_of_independents = len(x)
        if number_of_independents == 0:
            print("Preview of zero dimensional datasets is not implemented.")
            return

        if number_of_independents > 2:
            print(
                "Preview of three or higher dimensional datasets " "is not implemented."
            )
            return

        if np.any([x[i].type == "labeled" for i in range(len(x))]):
            print("Preview of labeled plots is not implemented.")
            return

        qapp = QtWidgets.QApplication(sys.argv)
        app = ApplicationWindow(data)
        app.show()
        sys.exit(qapp.exec_())
    else:
        _preview(data)


def _preview(data, *args, **kwargs):
    """Quick display of the data."""
    x = data.dimensions
    y = data.dependent_variables
    y_len = len(y)
    y_grid = int(y_len / 2) + 1

    if len(x) == 0:
        print("Preview of zero dimensional datasets is not implemented.")
        return

    if len(x) > 2:
        print("Preview of three or higher dimensional datasets " "is not implemented.")
        return

    if np.any([x[i].type == "labeled" for i in range(len(x))]):
        print("Preview of labeled plots is not implemented.")
        return

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
            if y[i].quantity_type in scalar:
                plot1D(x, y, i, ax, *args, **kwargs)
            if "vector" in y[i].quantity_type:
                vector_plot(x, y, i, fig, ax, *args, **kwargs)
            # if "audio" in y[i].quantity_type:
            #     audio(x, y, i, fig, ax, *args, **kwargs)

        plt.tight_layout(w_pad=0.0, h_pad=0.0)
        plt.show()

    if len(x) == 2:
        for i in range(y_len):
            # if y[i].quantity_type in ["RGB", "RGBA"]:
            #     RGB(x, y, i, fig, ax, *args, **kwargs)
            if y[i].quantity_type in scalar:
                twoD_scalar(x, y, i, fig, ax, *args, **kwargs)
            if "vector" in y[i].quantity_type:
                vector_plot(x, y, i, fig, ax, *args, **kwargs)

        plt.tight_layout(w_pad=0.0, h_pad=0.0)
        plt.show()


# =========================================================================== #


def plot1D(x, y, i0, ax, *args, **kwargs):
    i = int(i0 / 2)
    j = int(i0 % 2)
    components = y[i0].components.shape[0]
    for k in range(components):
        ax[i][j].plot(x[0].coordinates, y[i0].components[k].real, *args, **kwargs)
        if "complex" in y[i0].numeric_type:
            ax[i][j].plot(x[0].coordinates, y[i0].components[k].imag, *args, **kwargs)

        ax[i][j].set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
        ax[i][j].set_xlabel(x[0].axis_label)
        ax[i][j].set_ylabel(y[i0].axis_label[0])
        ax[i][j].set_title("{0}".format(y[i0].name))
        ax[i][j].grid(color="gray", linestyle="--", linewidth=0.5)


def RGB(x, y, i0, fig, ax, *args, **kwargs):
    i = int(i0 / 2)
    j = i0 % 2
    y0 = y[i0].components
    ax[i][j].imshow(np.moveaxis(y0 / y0.max(), 0, -1), *args, **kwargs)
    ax[i][j].set_title("{0}".format(y[i0].name))


def twoD_scalar(x, y, i0, fig, ax, *args, **kwargs):
    i = int(i0 / 2)
    j = i0 % 2

    x0 = x[0].coordinates.value
    x1 = x[1].coordinates.value
    y00 = y[i0].components[0].astype(np.float64)
    extent = [x0.min(), x0.max(), x1.min(), x1.max()]
    if x[0].type == "linear" and x[1].type == "linear":
        # print('uniform')
        cs = ax[i][j].imshow(
            y00.real, extent=extent, origin="lower", aspect="auto", *args, **kwargs
        )
    else:
        # print('non-uniform')
        cs = NonUniformImage(
            ax[i][j], interpolation="none", extent=extent, *args, **kwargs
        )
        cs.set_data(x0, x1, y00.real / y00.real.max())
        ax[i][j].images.append(cs)

    cbar = fig.colorbar(cs, ax=ax[i][j])
    cbar.ax.minorticks_off()
    cbar.set_label(y[i0].axis_label[0])
    ax[i][j].set_xlim([extent[0], extent[1]])
    ax[i][j].set_ylim([extent[2], extent[3]])
    ax[i][j].set_xlabel(x[0].axis_label)
    ax[i][j].set_ylabel(x[1].axis_label)
    ax[i][j].set_title("{0}".format(y[i0].name))
    ax[i][j].grid(color="gray", linestyle="--", linewidth=0.5)


def vector_plot(x, y, i0, fig, ax, *args, **kwargs):
    i = int(i0 / 2)
    j = i0 % 2
    x0 = x[0].coordinates.value
    if len(x) == 2:
        x1 = x[1].coordinates.value
    else:
        x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y[i0].components[0]
    v1 = y[i0].components[1]
    ax[i][j].quiver(x0, x1, u1, v1, pivot="middle", *args, **kwargs)
    ax[i][j].set_xlabel(x[0].axis_label)
    ax[i][j].set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
    if len(x) == 2:
        ax[i][j].set_ylim(x[1].coordinates.value.min(), x[1].coordinates.value.max())
        ax[i][j].set_ylabel(x[1].axis_label)
    else:
        ax[i][j].set_ylim([-y[i0].components.max(), y[i0].components.max()])
    ax[i][j].set_title("{0}".format(y[i0].name))
    ax[i][j].grid(color="gray", linestyle="--", linewidth=0.5)


def audio(x, y, i0, fig, ax):
    try:
        SOUND = 1
        import sounddevice as sd
    except ImportError:
        SOUND = 0
        string = (
            "Module 'sounddevice' is not installed. All audio data files will "
            "not be played. To enable audio files, install 'sounddevice' using"
            " 'pip install sounddevice'."
        )
        warn(string)

    plot1D(x, y, i0, ax)
    if SOUND == 1:
        data_max = y[i0].components.max()
        sd.play(0.9 * y[i0].components.T / data_max, 1 / x[0].increment.to("s").value)


# =========================================================================== #


def plot_line(x, y, ax):
    components = y.components.shape[0]
    for k in range(components):
        ax.plot(x[0].coordinates, y.components[k].T.real)
        if "complex" in y.numeric_type:
            ax.plot(x[0].coordinates, y.components[k].T.imag)

        if x[0].type != "labeled":
            ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())

        ax.set_xlabel(x[0].axis_label)
        ax.set_ylabel(y.axis_label[0])
        ax.set_title("{0}".format(y.name))
        ax.grid(color="gray", linestyle="-", linewidth=0.5)


def plot_image(x, y, fig, ax):
    # if x[0].type != 'labeled':
    #     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    #             x[1].coordinates[0].value, x[1].coordinates[-1].value]

    x0 = x[0].coordinates.value
    x1 = x[1].coordinates.value
    y00 = y.components[0].real.astype(np.float64)
    extent = [x0.min(), x0.max(), x1.min(), x1.max()]
    if x[0].type == "linear" and x[1].type == "linear":
        # print('uniform')
        cs = ax.imshow(y00, extent=extent, origin="lower", aspect="auto", cmap="Blues")
    else:
        # print('non-uniform')
        cs = NonUniformImage(ax, interpolation="nearest", extent=extent, cmap="bone_r")
        cs.set_data(x0, x1, y00 / y00.max())
        ax.images.append(cs)

    # cs = ax.imshow(
    #           y00,
    #           extent=extent,
    #           origin='lower',
    #           aspect='auto',
    #           cmap='viridis',
    #           interpolation='none'
    # )
    cbar = fig.colorbar(cs, ax=ax)
    cbar.ax.minorticks_off()
    cbar.set_label(y.axis_label[0])

    ax.set_xlim([extent[0], extent[1]])
    ax.set_ylim([extent[2], extent[3]])

    ax.set_xlabel(x[0].axis_label)
    ax.set_ylabel(x[1].axis_label)
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.1)


def plot_vector(x, y, ax):
    #     i = int(i0/2); j=i0%2
    if x[0].type != "labeled":
        x0 = x[0].coordinates.value
        if len(x) == 2:
            x1 = x[1].coordinates.value
        else:
            x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y.components[0]
    v1 = y.components[1]
    ax.quiver(x0, x1, u1, v1, pivot="middle")
    ax.set_xlabel(x[0].axis_label)
    ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
    if len(x) == 2:
        ax.set_ylim(x[1].coordinates.value.min(), x[1].coordinates.value.max())
        ax.set_ylabel(x[1].axis_label)
    else:
        ax.set_ylim([-y.components.max(), y.components.max()])
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.5)


def plot_RGB(x, y, ax):
    y0 = y.components
    ax.imshow(np.moveaxis(y0 / y0.max(), 0, -1))
    ax.set_title("{0}".format(y.name))


def plot_audio(x, y, ax):
    try:
        SOUND = 1
        import sounddevice as sd
    except ImportError:
        SOUND = 0
        string = (
            "Module 'sounddevice' is not installed. All audio data files will "
            "not be played. To enable audio files, install 'sounddevice' using"
            " 'pip install sounddevice'."
        )
        warn(string)

    plot_line(x, y, ax)
    # print (SOUND)
    if SOUND == 1:
        data_max = y.components.max()
        sd.play(0.9 * y.components.T / data_max, 1 / x[0].increment.to("s").value)


try:

    class ApplicationWindow(QtWidgets.QMainWindow):
        def __init__(self, dictionary):
            super().__init__()
            self._main = QtWidgets.QWidget()
            self._main.setWindowTitle(dictionary.filename)
            self.setCentralWidget(self._main)
            tabs = QtWidgets.QTabWidget(self._main)
            layout = QtWidgets.QVBoxLayout(self._main)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)

            # def display(event_location):
            #     print('x={0}, y={1}, xdata={2}, ydata={3}'.format( \
            #         event_location.x, event_location.y,
            #         event_location.xdata, event_location.ydata))

            def key_event(event):
                pass
                # print("you pressed", event.button, event.xdata, event.ydata)
                # im = ax.get_images()[0]
                # limits = im.get_clim()
                # im.set_clim(limits/2)

            def set_gui():
                tab_ = QtWidgets.QWidget()
                layout_ = QtWidgets.QVBoxLayout(tab_)
                layout_.setSpacing(0)
                layout_.setContentsMargins(0, 0, 0, 0)
                canvas = FigureCanvas(Figure(tight_layout=True))  # figsize=(5, 3),
                layout_.addWidget(canvas)
                layout_.addWidget(NavigationToolbar(canvas, self))
                tabs.addTab(tab_, "Dependent variable {0}".format(str(i)))

                ax = canvas.figure.subplots()
                # cid = canvas.mpl_connect("button_press_event", key_event)
                fig = canvas.figure
                return fig, ax

            number_of_dependents = len(dictionary.dependent_variables)
            number_of_independents = len(dictionary.dimensions)

            for i in range(number_of_dependents):
                # tab_.append(QtWidgets.QWidget())
                # layout_.append(QtWidgets.QVBoxLayout(tab_[-1]))
                # layout_[-1].setSpacing(0)
                # layout_[-1].setContentsMargins(0,0,0,0)
                # canvas = FigureCanvas(Figure(tight_layout=True))
                # layout_[-1].addWidget(canvas)
                # layout_[-1].addWidget(NavigationToolbar(canvas, self))
                # tabs.addTab(tab_[-1], f'Dependent variable {i}')

                # ax = canvas.figure.subplots()
                # fig = canvas.figure
                # cid = canvas.mpl_connect('axes_enter_event', display)

                x = dictionary.dimensions
                y = dictionary.dependent_variables[i]

                if number_of_independents == 1:

                    if y.quantity_type in scalar:
                        fig, ax = set_gui()
                        plot_line(x, y, ax)
                    # if "audio" in y.quantity_type:
                    #     fig, ax = set_gui()
                    #     plot_audio(x, y, ax)
                    if y.quantity_type == "vector_2":
                        fig, ax = set_gui()
                        plot_vector(x, y, ax)

                if number_of_independents == 2:
                    print(y.quantity_type)
                    if y.quantity_type in scalar:
                        fig, ax = set_gui()
                        if np.any([x[i].type == "labeled" for i in [0, 1]]):
                            plot_line(x, y, ax)
                        else:
                            print("plot image")
                            plot_image(x, y, fig, ax)
                    if y.quantity_type == "vector_2":
                        fig, ax = set_gui()
                        plot_vector(x, y, ax)
                    # if y.quantity_type in ["RGB", "RGBA"]:
                    #     fig, ax = set_gui()
                    #     plot_RGB(x, y, ax)

                if number_of_independents > 2:
                    print(
                        "Preview of three or higher dimensional datasets "
                        "is not implemented."
                    )
            layout.addWidget(tabs)


except Exception:
    pass
