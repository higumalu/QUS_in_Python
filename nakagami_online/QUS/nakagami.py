import numpy as np


def nakagami_moment(blocks):
    blocks_np = np.array(blocks)  # Assuming blocks is a list or some other array-like structure
    mean_square = np.mean(blocks_np**2)
    est_value = mean_square**2 / np.mean((blocks_np**2 - mean_square)**2)
    return est_value