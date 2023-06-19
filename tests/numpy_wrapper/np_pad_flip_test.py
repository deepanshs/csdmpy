import numpy as np

import csdmpy as cp


def test_1():
    test_a = np.arange(10 * 40).reshape(10, 40)
    csdm = cp.as_csdm(test_a)
    csdm_pad = np.pad(csdm, (2, 3))

    np.testing.assert_allclose(csdm_pad.x[1].coordinates, np.arange(15) - 2)
    np.testing.assert_allclose(csdm_pad.x[0].coordinates, np.arange(45) - 2)

    csdm_pad = np.pad(csdm, ((2, 3), (1, 4)))
    np.testing.assert_allclose(csdm_pad.x[1].coordinates, np.arange(15) - 1)
    np.testing.assert_allclose(csdm_pad.x[0].coordinates, np.arange(45) - 2)


def test_flip():
    test_a = np.arange(10 * 40).reshape(10, 40)
    csdm = cp.as_csdm(test_a)
    csdm_pad = np.flip(csdm)

    np.testing.assert_allclose(np.argmax(csdm_pad), 0)
