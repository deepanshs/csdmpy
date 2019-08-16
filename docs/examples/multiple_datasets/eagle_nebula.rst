.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path


Astronomy, 2D{1,1,1} dataset (Creating image composition)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More often the image in astronomy is a composition of datasets measured
at a different wavelength over an area of the sky. Here, we show an example
of an image composition using the data from the `Eagle Nebula`.
Import the `csdmpy` model and load the dataset.

.. doctest::

    >>> import csdmpy as cp
    >>> import matplotlib.pyplot as plt

    >>> filename = 'Test Files/EagleNebula/eagleNebula.csdfe'
    >>> eagle_nebula = cp.load(filename)

Let's get the tuple of dimension and dependent variable objects from
``eagle_nebula`` instance.

.. doctest::

    >>> x = eagle_nebula.dimensions
    >>> y = eagle_nebula.dependent_variables

Before we create an image composition, let's take a look at the individual
dependent variables from the dataset. The three dependent variables correspond
to signal acquisition at 502 nm, 656 nm, and 673 nm, respectively. This
information is also listed in the
:attr:`~csdmpy.dependent_variables.DependentVariable.name` attribute of the
respective dependent variable instances,

.. doctest::

    >>> y[0].name
    'Eagle Nebula acquired @ 502 nm'
    >>> y[1].name
    'Eagle Nebula acquired @ 656 nm'
    >>> y[2].name
    'Eagle Nebula acquired @ 673 nm'

.. tip::

    A script to plot an intensity plot.

    .. doctest::

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits.axes_grid1 import make_axes_locatable
        >>> from matplotlib.colors import LogNorm

        >>> def plot_scalar(yx):
        ...     plt.figure(figsize=(6,4.5))
        ...
        ...     # Set the extents of the image plot.
        ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
        ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
        ...
        ...     # Add the image plot.
        ...     y0 = yx.components[0]
        ...     y0 = y0/y0.max()
        ...     im = plt.imshow(y0, origin='lower', extent=extent, cmap='bone', vmax=0.1)
        ...
        ...     # Add a colorbar.
        ...     divider = make_axes_locatable(plt.gca())
        ...     cax = divider.append_axes("right", size="5%", pad=0.05)
        ...     cbar = plt.gca().figure.colorbar(im, cax)
        ...     cbar.ax.set_ylabel(yx.axis_label[0])
        ...
        ...     # Set up the axes label and figure title.
        ...     plt.xlabel(x[0].axis_label)
        ...     plt.ylabel(x[1].axis_label)
        ...     plt.title(yx.name)
        ...
        ...     # Set up the grid lines.
        ...     plt.grid(color='k', linestyle='--', linewidth=0.5)
        ...
        ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        ...     plt.show()

.. testsetup::

    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.axes_grid1 import make_axes_locatable
    >>> from matplotlib.colors import LogNorm

    >>> def plot_scalar_save(yx, dataObject):
    ...     fig, ax = plt.subplots(1,1, figsize=(6,4.5))
    ...
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # Add the image plot.
    ...     y0 = yx.components[0]
    ...     y0 = y0/y0.max()
    ...     im = ax.imshow(y0, origin='lower', extent=extent, cmap='bone', vmax=0.1)
    ...
    ...     # Add a colorbar.
    ...     divider = make_axes_locatable(ax)
    ...     cax = divider.append_axes("right", size="5%", pad=0.05)
    ...     cbar = fig.colorbar(im, cax)
    ...     cbar.ax.set_ylabel(yx.axis_label[0])
    ...
    ...     # Set up the axes label and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(yx.name)
    ...
    ...     # Set up the grid lines.
    ...     ax.grid(color='k', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+yx.name.replace(' ', '')+'.pdf')
    ...     plt.savefig(pth+yx.name.replace(' ', '')+'.png', dpi=100)
    ...     plt.close()

Let's plot the dependent variables, first dependent variable,

.. doctest::

    >>> plot_scalar(y[0])

.. testsetup::

    >>> plot_scalar_save(y[0], eagle_nebula)

.. figure:: ../../_images/eagleNebula.csdfeEagleNebulaacquired@502nm.*
    :figclass: figure-polaroid

second dependent variable, and

.. doctest::

    >>> plot_scalar(y[1])

.. testsetup::

    >>> plot_scalar_save(y[1], eagle_nebula)

.. figure:: ../../_images/eagleNebula.csdfeEagleNebulaacquired@656nm.*
    :figclass: figure-polaroid

the third dependent variable.

.. doctest::

    >>> plot_scalar(y[2])

.. testsetup::

    >>> plot_scalar_save(y[2], eagle_nebula)

.. figure:: ../../_images/eagleNebula.csdfeEagleNebulaacquired@673nm.*
    :figclass: figure-polaroid

Image composition
*****************

In our image composition, we will assign the dependent variable at index 0 as
the blue channel, at index 1 as the green channel, and index 2 as the red
channel of an RGB image. First, create an empty array to hold the RGB dataset.

.. doctest::

    >>> shape = y[0].components[0].shape + (3,)
    >>> image = np.empty(shape, dtype=np.float64)

Here, ``image`` is a variable we use for storing the composition. Let's add the
respective dependent variables to the designated color channel in the
``image`` array,

.. doctest::

    >>> image[...,0] = y[2].components[0]/y[2].components[0].max() # red channel
    >>> image[...,1] = y[1].components[0]/y[1].components[0].max() # green channel
    >>> image[...,2] = y[0].components[0]/y[0].components[0].max() # blue channel

If you follow the above figures, the component intensity from
``y[1]`` and, therefore, the green channel dominates the other two. If we
plot the ``image`` data, the image will be saturated with green intensity. To
attain a color-balanced image, we arbitrarily scale the intensities from the
three channels. You may choose any scaling factor. Each scaling factor will
produce a different composition. In this example, we use the following,

.. doctest::

    >>> image[...,0] = image[...,0]*65.0 # red channel
    >>> image[...,1] = image[...,1]*7.5  # green channel
    >>> image[...,2] = image[...,2]*75.0 # blue channel

Now to plot this composition.

.. doctest::

    >>> def image_composition():
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # add figure
    ...     plt.figure(figsize=(5,4.5))
    ...     plt.imshow(image, origin='lower', extent=extent)
    ...
    ...     plt.xlabel(x[0].axis_label)
    ...     plt.ylabel(x[1].axis_label)
    ...     plt.title('composition')
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     plt.show()

.. testsetup::

    >>> def image_composition_save(dataObject):
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # add figure
    ...     plt.figure(figsize=(5,4.5))
    ...     plt.imshow(image, origin='lower', extent=extent)
    ...
    ...     plt.xlabel(x[0].axis_label)
    ...     plt.ylabel(x[1].axis_label)
    ...     plt.title('composition')
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+'composition'+'.pdf')
    ...     plt.savefig(pth+'composition'+'.png', dpi=100)
    ...     plt.close()

.. doctest::

    >>> image_composition()

.. testsetup::

    >>> image_composition_save(eagle_nebula)

.. figure:: ../../_images/eagleNebula.csdfecomposition.*
    :figclass: figure-polaroid
