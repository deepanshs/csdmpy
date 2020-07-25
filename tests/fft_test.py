# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp


def fft_process(csdm):

    y = csdm.dependent_variables[0].components[0]

    # fft
    coordinates_offset = csdm.dimensions[0].coordinates_offset
    reciprocal_coordinates = csdm.dimensions[0].reciprocal_coordinates()

    phase = np.exp(-2j * np.pi * coordinates_offset * reciprocal_coordinates)
    y_fft = np.fft.fftshift(np.fft.fft(y)) * phase
    csdm_fft = csdm.fft(axis=0)
    assert np.allclose(y_fft, csdm_fft.dependent_variables[0].components[0])

    # inverse fft
    reciprocal_coordinates_offset = csdm_fft.dimensions[0].reciprocal.coordinates_offset
    coordinates = csdm_fft.dimensions[0].coordinates

    phase = np.exp(2j * np.pi * reciprocal_coordinates_offset * coordinates)
    y2 = np.fft.ifft(np.fft.ifftshift(y_fft * phase))
    csdm_2 = csdm_fft.fft(axis=0)

    assert np.allclose(y, y2)
    assert np.allclose(y2, csdm_2.dependent_variables[0].components[0])
    assert csdm == csdm_2


def ifft_process(csdm):

    y = csdm.dependent_variables[0].components[0]

    # inverse fft
    reciprocal_coordinates_offset = csdm.dimensions[0].reciprocal.coordinates_offset
    coordinates = csdm.dimensions[0].coordinates - csdm.dimensions[0].coordinates_offset

    phase = np.exp(2j * np.pi * reciprocal_coordinates_offset * coordinates)
    y_fft = np.fft.ifft(np.fft.ifftshift(y * phase))
    csdm_fft = csdm.fft(axis=0)

    assert np.allclose(y_fft, csdm_fft.dependent_variables[0].components[0])

    # fft
    coordinates_offset = csdm_fft.dimensions[0].coordinates_offset
    reciprocal_coordinates = csdm_fft.dimensions[0].reciprocal_coordinates()

    phase = np.exp(-2j * np.pi * coordinates_offset * reciprocal_coordinates)
    y2 = np.fft.fftshift(np.fft.fft(y_fft)) * phase
    csdm_2 = csdm_fft.fft(axis=0)

    assert np.allclose(y, y2)
    assert np.allclose(y2, csdm_2.dependent_variables[0].components[0])
    assert csdm == csdm_2


def test_fft_1():

    for _ in range(10):
        coordinates = np.arange(64, dtype=np.float64) - (np.random.rand() * 64)
        vals = np.random.rand(64).astype(np.complex128)

        csdm = cp.new()
        csdm.add_dimension(cp.as_dimension(coordinates))
        csdm.add_dependent_variable(
            cp.as_dependent_variable(vals, quantity_type="scalar")
        )

        fft_process(csdm)


def test_fft_2():

    for _ in range(10):
        coordinates = np.arange(64, dtype=np.float64) - (np.random.rand() * 64)
        vals = np.random.rand(64).astype(np.complex128)

        csdm = cp.new()
        csdm.add_dimension(cp.as_dimension(coordinates, complex_fft=True))
        csdm.add_dependent_variable(
            cp.as_dependent_variable(vals, quantity_type="scalar")
        )

        ifft_process(csdm)
