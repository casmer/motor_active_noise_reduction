#!/usr/bin/env python3
import sounddevice as sd
import numpy as np

from scipy.signal import butter, lfilter
import scipy.io.wavfile as wav

import sys
fs = 44100
# Filter requirements.
order = 6

cutoff = 1000  # desired cutoff frequency of the filter, Hz



class NoiseReducer(object):
    def __init__(self):
        self.first_pass = True
        self.fs = 44100
        # Filter requirements.
        self.order = 6

        self.cutoff = 1000
        
    def butter_lowpass(self, cutoff, fs, order=5):
        return butter(order, cutoff, fs=fs, btype='low', analog=False)

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def callback(self, indata, outdata, frames, time, status):
            
       
        outdata[:] = -self.butter_lowpass_filter(indata, self.cutoff, self.fs, self.order)


nr = NoiseReducer()

try:
    with sd.Stream(device=(1,1), samplerate=fs, dtype='float32', latency=None, channels=2, callback=nr.callback):
        input()
except KeyboardInterrupt:
    pass

# print ("reading file")
# fs, x = wav.read("./pump_hum.wav")
# print ("filtering file")
# result = -nr.butter_lowpass_filter(x, cutoff, fs, order)
# print ("writing file")
# wav.write("out.wav", fs, np.array(np.array(result) * 2.0 ** 15, dtype='int16'))
# for i in range(0,10):
#     print ("x[{}]={}".format(i,x))
#     print ("result[{}]={}".format(i,result))
# # result2 = np.sum(x, result)
# # wav.write("out2.wav", fs, np.array(np.array(result2) * 2.0 ** 15, dtype='int16'))
# print ("End")