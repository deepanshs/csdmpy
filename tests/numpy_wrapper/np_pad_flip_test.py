import numpy as np

import csdmpy as cp


def test_1_linear():
    test_a = np.arange(10 * 40).reshape(10, 40)
    csdm = cp.as_csdm(test_a)
    csdm_pad = np.pad(csdm, (2, 3))

    np.testing.assert_allclose(csdm_pad.x[1].coordinates, np.arange(15) - 2)
    np.testing.assert_allclose(csdm_pad.x[0].coordinates, np.arange(45) - 2)

    csdm_pad = np.pad(csdm, pad_width=((2, 3), (1, 4)))
    np.testing.assert_allclose(csdm_pad.x[1].coordinates, np.arange(15) - 1)
    np.testing.assert_allclose(csdm_pad.x[0].coordinates, np.arange(45) - 2)

    csdm_pad = np.pad(csdm, pad_width=5, constant_values=((500, -500), (1000, -1000)))
    np.testing.assert_allclose(csdm_pad[0, 0], 500)
    np.testing.assert_allclose(csdm_pad[49, 19], -500)

    csdm_pad = np.pad(csdm, pad_width=(5,))
    np.testing.assert_allclose(csdm_pad[0, 0], 0)
    np.testing.assert_allclose(csdm_pad[49, 19], 0)


def test_2_monotonic():
    array = np.arange(10 * 40).reshape(10, 40)
    d_v = cp.as_dependent_variable(array)
    d_1 = cp.as_dimension(np.exp(np.arange(10) / 10))
    d_2 = cp.as_dimension(np.arange(40))
    csdm = cp.CSDM(dimensions=[d_1, d_2], dependent_variables=[d_v])

    padded = np.pad(csdm, ((2, 3),))
    np.testing.assert_allclose(padded.x[0].coordinates[:2], [0.78965816, 0.89482908])


def test_3_labeled():
    array = np.arange(10 * 40).reshape(10, 40)
    d_v = cp.as_dependent_variable(array)
    d_1 = cp.as_dimension(["3"] * 2 + ["5"] * 7 + ["1"])
    d_2 = cp.as_dimension(np.arange(40))
    csdm = cp.CSDM(dimensions=[d_1, d_2], dependent_variables=[d_v])

    padded = np.pad(csdm, ((2, 3),))
    np.testing.assert_equal(padded.x[0].coordinates[:2], ["0", "0"])


def test_flip():
    test_a = np.arange(10 * 40).reshape(10, 40)
    csdm = cp.as_csdm(test_a)

    csdm_flip = np.flip(csdm)
    np.testing.assert_allclose(np.argmax(csdm_flip), 0)

    csdm_flip = np.flip(csdm, 1)
    np.testing.assert_allclose(np.argmax(csdm_flip), 39)

    csdm_flip = np.flip(csdm, axis=0)
    np.testing.assert_allclose(np.argmax(csdm_flip), 360)
