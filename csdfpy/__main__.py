# -*- coding: utf-8 -*-
"""CSDModel main."""
import sys

import csdfpy as cp
from csdfpy.helper_functions import preview


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


if __name__ == "__main__":
    for i in range(len(sys.argv) - 1):
        data = cp.load(sys.argv[i + 1])
        preview(data)
