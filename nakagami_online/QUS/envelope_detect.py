
import numpy as np
import scipy.signal as sg

###Hilbert trans
def hilbert_demod(rf):
    return abs(sg.hilbert2(rf))


###IQ demode
def AM_line(rfline, fs, fc):
    fs = fs*10e6
    fc = fc*10e6
    t = rfline.shape[0]/fs
    i = rfline * np.cos(2 * np.pi * fc * t) * 200
    q = rfline * np.sin(2 * np.pi * fc * t) * 200
    output = np.sqrt(i * i + q * q) 
    return output

def AM_demod(rf, fs=12, fc=4):
    datalength = rf.shape[0]
    alinenumber = rf.shape[1]
    evorf = np.zeros(shape=(int(datalength),alinenumber))
    for i in range(0,alinenumber):
        aline = rf[:,i]
        aline = AM_line(aline, fs, fc)
        evorf[:,i] = aline
    '''
    nyq_rate = fs / 2.
    cutoff_hz = nyq_rate
    numtaps = 11
    lpf = sg.firwin(numtaps, cutoff_hz / nyq_rate)
    i2 = sg.lfilter(lpf, 1, i1)
    q2 = sg.lfilter(lpf, 1, q1)
    o = np.sqrt(i2 * i2 + q2 * q2) 
    '''
    return evorf