# -*- coding: utf-8 -*-
"""CSDM main."""
import sys

import matplotlib.pyplot as plt

import csdmpy as cp
from csdmpy.helper_functions import _preview

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


if __name__ == "__main__":
    for i in range(len(sys.argv) - 1):
        data = cp.load(sys.argv[i + 1])
        _preview(data)
        plt.show()
