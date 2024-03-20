from copy import deepcopy

import numpy as np
import scipy as sp

import csdmpy as cp


def fft_process(csdm):
    y = csdm.y[0].components[0]

    # fft
    coordinates_offset = csdm.dimensions[0].coordinates_offset
    reciprocal_coordinates = csdm.dimensions[0].reciprocal_coordinates()

    scale = 1.0 if np.isfinite(csdm.dimensions[0].period) else 2.0
    phase = np.exp(-2j * np.pi * coordinates_offset * reciprocal_coordinates)
    y_copy = deepcopy(y)
    y_copy[0] /= scale
    y_fft = sp.fft.fftshift(sp.fft.fft(y_copy)) * phase
    csdm_fft = csdm.fft(axis=0)
    assert np.allclose(y_fft, csdm_fft.y[0].components[0])

    # inverse fft
    reciprocal_coordinates_offset = csdm_fft.dimensions[0].reciprocal.coordinates_offset
    coordinates = csdm_fft.dimensions[0].coordinates

    phase = np.exp(2j * np.pi * reciprocal_coordinates_offset * coordinates)
    y2 = sp.fft.ifft(sp.fft.ifftshift(y_fft * phase))
    y2[0] *= scale
    csdm_2 = csdm_fft.fft(axis=0)

    assert np.allclose(y, y2)
    assert np.allclose(y2, csdm_2.y[0].components[0])
    assert csdm == csdm_2


def ifft_process(csdm):
    y = csdm.y[0].components[0]

    # inverse fft
    reciprocal_coordinates_offset = csdm.dimensions[0].reciprocal.coordinates_offset
    coordinates = csdm.dimensions[0].coordinates - csdm.dimensions[0].coordinates_offset

    scale = 1.0 if np.isfinite(csdm.dimensions[0].period) else 2.0
    phase = np.exp(2j * np.pi * reciprocal_coordinates_offset * coordinates)

    y_fft = sp.fft.ifft(sp.fft.ifftshift(y * phase))
    y_fft[0] *= scale
    csdm_fft = csdm.fft(axis=0)

    assert np.allclose(y_fft, csdm_fft.y[0].components[0])

    # fft
    coordinates_offset = csdm_fft.dimensions[0].coordinates_offset
    reciprocal_coordinates = csdm_fft.dimensions[0].reciprocal_coordinates()

    phase = np.exp(-2j * np.pi * coordinates_offset * reciprocal_coordinates)
    y_fft[0] /= scale
    y2 = sp.fft.fftshift(sp.fft.fft(y_fft)) * phase
    csdm_2 = csdm_fft.fft(axis=0)

    assert np.allclose(y, y2)
    assert np.allclose(y2, csdm_2.y[0].components[0])
    assert csdm == csdm_2


def test_fft_1():
    for _ in range(10):
        coordinates = np.arange(64, dtype=np.float64) - (np.random.rand() * 64)
        vals = np.random.rand(64).astype(np.complex128)

        csdm = cp.CSDM(
            dimensions=[cp.as_dimension(coordinates)],
            dependent_variables=[
                (cp.as_dependent_variable(vals, quantity_type="scalar"))
            ],
        )

        fft_process(csdm)


def test_fft_2():
    for _ in range(10):
        coordinates = np.arange(64, dtype=np.float64) - (np.random.rand() * 64)
        vals = np.random.rand(64).astype(np.complex128)

        csdm = cp.CSDM(
            dimensions=[cp.as_dimension(coordinates, complex_fft=True)],
            dependent_variables=[
                cp.as_dependent_variable(vals, quantity_type="scalar")
            ],
        )

        ifft_process(csdm)


def test_fft_3():
    for _ in range(10):
        coordinates = np.arange(64, dtype=np.float64) - (np.random.rand() * 64)
        vals = np.random.rand(64).astype(np.complex128)

        csdm = cp.CSDM(
            dimensions=[cp.as_dimension(coordinates, period="1")],
            dependent_variables=[
                (cp.as_dependent_variable(vals, quantity_type="scalar"))
            ],
        )

        fft_process(csdm)


def test_fft_2D_1():
    test_data = np.ones((40, 50))
    csdm_object = cp.CSDM(
        dependent_variables=[cp.as_dependent_variable(test_data)],
        dimensions=[
            cp.LinearDimension(count=50, increment="1 m"),
            cp.LinearDimension(count=40, increment="1 s", period="5 s"),
        ],
    )
    csdm_object_fft = csdm_object.fft(axis=0)
    csdm_object_2 = cp.CSDM(
        dependent_variables=[cp.as_dependent_variable(np.ones(50))],
        dimensions=[cp.LinearDimension(count=50, increment="1 m")],
    )
    csdm_object_2_fft = csdm_object_2.fft()

    assert np.allclose(
        csdm_object_fft[:, 0].y[0].components,
        csdm_object_2_fft.y[0].components,
    )

    csdm_object_fft = csdm_object.fft(axis=1)

    csdm_object_1 = cp.CSDM(
        dependent_variables=[cp.as_dependent_variable(np.ones(40))],
        dimensions=[cp.LinearDimension(count=40, increment="1 s", period="5 s")],
    )
    csdm_object_1_fft = csdm_object_1.fft()

    assert np.allclose(
        csdm_object_fft[0].y[0].components,
        csdm_object_1_fft.y[0].components,
    )
