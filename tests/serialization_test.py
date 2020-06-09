# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp


def setup():
    csdm = cp.new()
    dimension1 = cp.as_dimension(np.arange(10))
    dimension2 = cp.as_dimension(np.arange(20))
    data = cp.as_dependent_variable(np.random.rand(20, 10))

    csdm.add_dimension(dimension1)
    csdm.add_dimension(dimension2)
    csdm.add_dependent_variable(data)

    return csdm


def test_application():

    csdm1 = setup()
    csdm1.application = {"test": "root"}
    csdm1.dimensions[0].application = {"test": "d0"}
    csdm1.dimensions[0].reciprocal.application = {"test": "reciprocal-d0"}
    csdm1.dimensions[1].application = {"test": "d1"}
    csdm1.dimensions[1].reciprocal.application = {"test": "reciprocal-d1"}
    csdm1.dependent_variables[0].application = {"test": "dv0"}

    csdm1.dependent_variables[0].encoding = "base64"
    csdm1.save("csdm1.csdf")

    csdm1_test = cp.load("csdm1.csdf", application=True)

    assert csdm1_test == csdm1
