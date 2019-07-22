# -*- coding: utf-8 -*-
"""CSDM main."""
import sys

import csdmpy as cp
from csdmpy.helper_functions import preview


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


if __name__ == "__main__":
    for i in range(len(sys.argv) - 1):
        data = cp.load(sys.argv[i + 1])
        preview(data)
