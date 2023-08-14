import numpy as np
from scipy.ndimage import zoom

from .nakagami import nakagami_moment


def ParametricMapping(setting, envelope, detect_method, windowsize):

    y = 0.5 * setting['soundspeed'] * (setting['pulselength'] / setting['samplingrate'])
    inte = round(setting['windowsize'][2] * setting['pulselength'])
    inte1 = round(setting['windowsize'][2] * (y / setting['scanstep']))
    
    envelope[envelope < setting['threshold']] = 0
    #localm1 = np.zeros(envelope.shape[:])  # Initialize localm1 as a numpy array
    #localm = np.zeros(envelope.shape[:])  # Initialize localm as a numpy array
    


    setting['wor'] = (100 - setting['wor']) / 100
    y = 0.5 * setting['soundspeed'] * (setting['pulselength'] / setting['samplingrate'])
    inte = round(setting['windowsize'][windowsize - 1] * setting['pulselength'])    #depth
    inte1 = round(setting['windowsize'][windowsize - 1] * (y / setting['scanstep']))    #width
    
    lateral_n = (setting['alinenumber'] - inte1) // round(inte1 * setting['wor']) + 1
    axial_n = (setting['datalength'] - inte) // round(inte * setting['wor']) + 1
    
    localm = np.zeros([axial_n, lateral_n])
    
    if detect_method == 'nakagami':
        ccc = 0
        for lateral_i in range(0, setting['alinenumber'] - inte1, round(inte1 * setting['wor'])):
            ddd = 0
            for axial_i in range(0, setting['datalength'] - inte, round(inte * setting['wor'])):
                block = envelope[axial_i:axial_i + inte + 1, lateral_i:lateral_i + inte1 + 1]
                blocks = block.ravel()

                localm[ddd, ccc] = nakagami_moment(blocks)

                if np.isnan(localm[ddd, ccc]):
                    localm[ddd, ccc] = 0
                if np.isinf(localm[ddd, ccc]):
                    localm[ddd, ccc] = 0
                ddd += 1

            # print(f"Progress: {ccc / (setting['alinenumber'] - inte1) * 100:.2f}%")
            ccc += 1

        # Using scipy's zoom as a replacement for MATLAB's imresize
        localm1 = zoom(localm, (setting['datalength'] / localm.shape[0], setting['alinenumber'] / localm.shape[1]))

    return localm1








