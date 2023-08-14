from .terason_read import read_mat
from .envelope_detect import hilbert_demod
from .shiftwin import ParametricMapping
from .fanout import scan_conversion


import matplotlib.pyplot as plt
import numpy as np

def calc_image(file_path):


    MHz = 10**6
    mm = 10**(-3)
    cm = 10**(-2)
    um = 10**(-6)
    us = 10**(-6)

    setting = {
        'centerfreq': 3.5 * MHz, 
        'intepolationfactor': 1,
        'samplingrate': 12 * MHz * 1,
        'soundspeed': 1540,
        'pulselength': 3 * us * 12 * MHz * 1,
        'threshold': 0,
        'windowsize': list(range(1, 21)),
        'wor': 50,
        'fftpoint': 1024,
        'lowerBW': 1 * MHz,
        'upperBW': 5.5 * MHz,
        'imagewidth': 10 * cm,
        'bmodeDR': 40,
        'compressionFactor': 70,
        'curveangle': 59,
        'fansize_width': 600,
        'fansize_height': 450,
        'fusiontransparency': 0.5,
        'compoundingindex': 7,
        'attenuationcoefficient': 0.5
    }
    

    RF = read_mat(file_path)


    setting['datalength'] = RF.shape[0]
    setting['alinenumber'] = RF.shape[1]
    setting['scanstep'] = setting['imagewidth'] / setting['alinenumber']
    setting['depth'] = [1000 * setting['soundspeed'] * 0.5 * ((i + 1) / setting['samplingrate']) for i in range(setting['datalength'])]


    env = hilbert_demod(RF)
    
    m = ParametricMapping(setting, env, 'nakagami', setting['windowsize'][3])
    bmode = 20*np.log10((10**(38/20)-1)*(env/np.max(env)) + 1)

    return m, bmode




def QUS_fig_save(paramap, bmode, dir):


    plt.figure(figsize=(8, 6))
    para_img = plt.imshow(paramap, cmap='jet', vmin=0, vmax=2)
    cbar = plt.colorbar(para_img, fraction=0.046, pad=0.04)
    cbar.set_label('Nakagami-m')
    plt.savefig(dir+'imgQUS.png', dpi=600, bbox_inches='tight')

    plt.figure(figsize=(8, 6))
    b_img = plt.imshow(bmode, cmap='gray')
    cbar = plt.colorbar(b_img, fraction=0.046, pad=0.04)
    cbar.set_label('Brightness')
    plt.savefig(dir+'imgB.png', dpi=600, bbox_inches='tight')


    plt.figure(figsize=(8, 6))
    b_img = plt.imshow(bmode, cmap='gray')
    para_img = plt.imshow(paramap, cmap='jet', vmin=0, vmax=2, alpha=0.3)
    cbar = plt.colorbar(para_img, fraction=0.046, pad=0.04)
    cbar.set_label('Nakagami-m')
    plt.savefig(dir+'fusion_img.png', dpi=600, bbox_inches='tight')


    fan_b_img, xxx, yyy = scan_conversion(bmode,60,600,450,80)
    fan_para_img, xxx, yyy = scan_conversion(paramap,60,600,450,80)

    plt.figure(figsize=(8, 6))
    # Plot the B-mode image and save it as fan_b_img.png
    fan_b_img_fu = plt.imshow(fan_b_img, extent=[xxx[0] / 10, xxx[-1] / 10, yyy[-1] / 10, yyy[0] / 10], cmap='gray')
    cbar = plt.colorbar(fan_b_img_fu, fraction=0.046, pad=0.04)
    cbar.set_label('Brightness')
    plt.xlabel('X (cm)')
    plt.ylabel('Y (cm)')
    plt.savefig(dir+'fan_b_img.png', dpi=600, bbox_inches='tight')
    plt.clf()  # Clear the figure for the next plot

    # Plot the fused image
    plt.imshow(fan_b_img, extent=[xxx[0] / 10, xxx[-1] / 10, yyy[-1] / 10, yyy[0] / 10], cmap='gray')
    fan_para_img_fu = plt.imshow(fan_para_img, extent=[xxx[0] / 10, xxx[-1] / 10, yyy[-1] / 10, yyy[0] / 10], cmap='jet', vmin=0, vmax=2, alpha=0.3)
    cbar = plt.colorbar(fan_para_img_fu, fraction=0.046, pad=0.04)
    cbar.set_label('Nakagami-m')
    plt.xlabel('X (cm)')
    plt.ylabel('Y (cm)')
    plt.savefig(dir+'fan_fusion_img.png', dpi=600, bbox_inches='tight')


'''
img_path = 'D:/TYLresearch/nakagami_online/upload_data/1.mat'
img_m, img_bmode = calc_image(img_path)

QUS_fig_save(img_m, img_bmode, 'D:/TYLresearch/nakagami_online/QUS/result/')
'''