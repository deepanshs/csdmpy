import numpy as np

import csdmpy as cp


def setup_reference_offset(offset):
    a = cp.LinearDimension(
        count=6, increment="1", coordinates_offset=f"{offset}", complex_fft=True
    )
    array = np.asarray([-3, -2, -1, 0, 1, 2]) + offset
    assert np.allclose(a.coordinates, array)
    assert a.get_nmr_reference_offset() == offset

    b = cp.LinearDimension(count=6, increment="1", coordinates_offset=f"{-3 + offset}")
    assert np.allclose(b.coordinates, array)
    assert b.get_nmr_reference_offset() == offset

    b = cp.LinearDimension(count=6, increment="-1", coordinates_offset=f"{2+offset}")
    assert np.allclose(b.coordinates, np.asarray([2, 1, 0, -1, -2, -3]) + offset)
    assert b.get_nmr_reference_offset() == offset

    b = cp.LinearDimension(count=5, increment="-1", coordinates_offset=f"{2 + offset}")
    assert np.allclose(b.coordinates, np.asarray([2, 1, 0, -1, -2]) + offset)
    assert b.get_nmr_reference_offset() == offset

    b = cp.LinearDimension(count=5, increment="1", coordinates_offset=f"{-2 + offset}")
    assert np.allclose(b.coordinates, np.asarray([-2, -1, 0, 1, 2]) + offset)
    assert b.get_nmr_reference_offset() == offset


def test_00():
    setup_reference_offset(0)
    setup_reference_offset(10)
    setup_reference_offset(-12.12)
    setup_reference_offset(61.12)
