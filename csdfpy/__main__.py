
"""CSDModel main."""
import sys
import csdfpy as cp
from csdfpy.helper_functions import quick_preview
try:
    import pyqtgraph as pg
except:
    import matplotlib.pyplot as plt

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

    
if __name__ == "__main__":
    # print('Argument List:', str(sys.argv))

    for i in range(len(sys.argv)-1):
        data = cp.load(sys.argv[i+1])
        quick_preview(data)



