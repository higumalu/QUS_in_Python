import math
import numpy as np
import scipy.io

def read_mat(matpath):
    mat = scipy.io.loadmat(matpath)
    rfarray = mat.get('b_data0')
    return rfarray




