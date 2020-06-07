# -*- coding: utf-8 -*-
"""Helper functions."""
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import NonUniformImage

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

scalar = ["scalar", "vector_1", "pixel_1", "matrix_1_1", "symmetric_matrix_1"]


def _preview(data, reverse_axis=None, range_=None, **kwargs):
    """Quick display of the data."""
    if reverse_axis is not None:
        kwargs["reverse_axis"] = reverse_axis

    if range_ is None:
        range_ = [[None, None], [None, None]]

    x = data.dimensions
    y = data.dependent_variables
    y_len = len(y)
    y_grid = int(y_len / 2) + 1

    if len(x) == 0:
        raise NotImplementedError(
            "Preview of zero dimensional datasets is not implemented."
        )

    if len(x) > 2:
        raise NotImplementedError(
            "Preview of three or higher dimensional datasets " "is not implemented."
        )

    if np.any([x[i].type == "labeled" for i in range(len(x))]):
        raise NotImplementedError("Preview of labeled dimensions is not implemented.")

    fig = plt.gcf()
    if y_len <= 2:
        ax = fig.subplots(y_grid)
        ax = [[ax]] if y_len == 1 else [ax]
    else:
        ax = fig.subplots(y_grid, 2)

    if len(x) == 1:
        one_d_plots(ax, x, y, range_, **kwargs)

    if len(x) == 2:
        two_d_plots(ax, x, y, range_, **kwargs)

    return fig


def one_d_plots(ax, x, y, range_, **kwargs):
    """A collection of possible 1D plots."""
    for i, y_item in enumerate(y):
        i0 = int(i / 2)
        j0 = int(i % 2)
        ax_ = ax[i0][j0]

        if y_item.quantity_type in scalar:
            oneD_scalar(x, y_item, ax_, range_, **kwargs)
        if "vector" in y_item.quantity_type:
            vector_plot(x, y_item, ax_, range_, **kwargs)
        # if "audio" in y_item.quantity_type:
        #     audio(x, y, i, fig, ax, **kwargs)


def two_d_plots(ax, x, y, range_, **kwargs):
    """A collection of possible 2D plots."""
    for i, y_item in enumerate(y):
        i0 = int(i / 2)
        j0 = int(i % 2)
        ax_ = ax[i0][j0]

        if y_item.quantity_type == "pixel_3":
            warn("This method interprets the `pixel_3` dataset as an RGB image.")
            RGB_image(x, y_item, ax_, range_, **kwargs)

        if y_item.quantity_type in scalar:
            twoD_scalar(x, y_item, ax_, range_, **kwargs)

        if "vector" in y_item.quantity_type:
            vector_plot(x, y_item, ax_, range_, **kwargs)


def oneD_scalar(x, y, ax, range_, **kwargs):
    reverse = [False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    components = y.components.shape[0]
    for k in range(components):
        ax.plot(x[0].coordinates, y.components[k], **kwargs)
        ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
        ax.set_xlabel(f"{x[0].axis_label} - 0")
        ax.set_ylabel(y.axis_label[0])
        ax.set_title("{0}".format(y.name))
        ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()


def twoD_scalar(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    x0 = x[0].coordinates.value
    x1 = x[1].coordinates.value
    y00 = y.components[0]
    extent = [x0[0], x0[-1], x1[0], x1[-1]]
    if "extent" not in kwargs.keys():
        kwargs["extent"] = extent

    if x[0].type == "linear" and x[1].type == "linear":
        if "origin" not in kwargs.keys():
            kwargs["origin"] = "lower"
        if "aspect" not in kwargs.keys():
            kwargs["aspect"] = "auto"

        cs = ax.imshow(y00, **kwargs)
    else:
        if "interpolation" not in kwargs.keys():
            kwargs["interpolation"] = "nearest"

        cs = NonUniformImage(ax, **kwargs)
        cs.set_data(x0, x1, y00)
        ax.images.append(cs)

    cbar = ax.figure.colorbar(cs, ax=ax)
    cbar.ax.minorticks_off()
    cbar.set_label(y.axis_label[0])
    ax.set_xlim([extent[0], extent[1]])
    ax.set_ylim([extent[2], extent[3]])
    ax.set_xlabel(f"{x[0].axis_label} - 0")
    ax.set_ylabel(f"{x[1].axis_label} - 1")
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()
    if reverse[1]:
        ax.invert_yaxis()


def vector_plot(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    x0 = x[0].coordinates.value
    if len(x) == 2:
        x1 = x[1].coordinates.value
    else:
        x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y.components[0]
    v1 = y.components[1]

    if "pivot" not in kwargs.keys():
        kwargs["pivot"] = "middle"
    ax.quiver(x0, x1, u1, v1, **kwargs)
    ax.set_xlabel(f"{x[0].axis_label} - 0")
    ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
    if len(x) == 2:
        ax.set_ylim(x[1].coordinates.value.min(), x[1].coordinates.value.max())
        ax.set_ylabel(f"{x[1].axis_label} - 1")
        if reverse[1]:
            ax.invert_yaxis()
    else:
        ax.set_ylim([-y.components.max(), y.components.max()])
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()


def RGB_image(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    y0 = y.components
    ax.imshow(np.moveaxis(y0 / y0.max(), 0, -1), **kwargs)
    ax.set_title("{0}".format(y.name))

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()
    if reverse[1]:
        ax.invert_yaxis()


# def audio(x, y, i0, fig, ax):
#     try:
#         SOUND = 1
#         import sounddevice as sd
#     except ImportError:
#         SOUND = 0
#         string = (
#             "Module 'sounddevice' is not installed. All audio data files will "
#             "not be played. To enable audio files, install 'sounddevice' using"
#             " 'pip install sounddevice'."
#         )
#         warn(string)

#     plot1D(x, y, i0, ax)
#     if SOUND == 1:
#         data_max = y[i0].components.max()
#         sd.play(0.9 * y[i0].components.T / data_max, 1 / x[0].increment.to("s").value)
