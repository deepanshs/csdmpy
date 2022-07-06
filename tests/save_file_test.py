from os import remove

import csdmpy as cp


def setup():
    d_x = cp.Dimension(type="labeled", labels=["🍈", "🍉", "🍋", "🍌", "🥑", "🍍"])
    d_y = cp.DependentVariable(
        type="internal",
        numeric_type="float32",
        quantity_type="scalar",
        components=[[0.5, 0.25, 1, 2, 1, 0.25]],
    )
    data = cp.CSDM(
        description="An emoji dataset", dimensions=[d_x], dependent_variables=[d_y]
    )
    return data


def test_csdf_base64():
    data = setup()
    data.save("my_file_base64.csdf")
    remove("my_file_base64.csdf")


def test_csdf_none():
    data = setup()
    data.y[0].encoding = "none"
    data.save("my_file_none.csdf")
    remove("my_file_none.csdf")


def test_csdfe():
    data = setup()
    data.y[0].encoding = "raw"
    data.save("my_file_raw.csdfe")
    remove("my_file_raw.csdfe")
    remove("my_file_raw_0.dat")
