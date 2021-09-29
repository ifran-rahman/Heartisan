##BEAT cutting
import numpy as np
from biosppy import storage
from biosppy.signals import ecg
import os
import wfdb as wf

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd


# import required modules
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model


def beatcutting(channel):


    channel = [int(i) for i in channel]
    out = ecg.ecg(signal=channel, sampling_rate=360, show=False)
    rpeaks = np.zeros_like(channel, dtype='float')
    rpeaks[out['rpeaks']] = 1.0
    beats = np.split(channel, out['rpeaks'])
    beatstoremove = np.array([0])

    signallength = len(beats)
    for idx in range(0,signallength-1):
        # Append some extra readings from next beat.
        beats[idx] = np.append(beats[idx], beats[idx+1][:40])

        # Normalize the readings to a 0-1 range for ML purposes.
        beats[idx] = (beats[idx] - beats[idx].min()) / beats[idx].ptp()

        # Resample from 360Hz to 125Hz
        newsize = int((beats[idx].size * 125 /360) + 0.5)
        beats[idx] = signal.resample(beats[idx], newsize)


        # Skipping records that are too long.
        if (beats[idx].size > 187):
            beatstoremove = np.append(beatstoremove, idx)
            continue

            # Pad with zeroes.
        zerocount = 187 - beats[idx].size
        beats[idx] = np.pad(beats[idx], (0, zerocount), 'constant', constant_values=(0.0, 0.0))
    return beats

def getIndex(enteredtime, dataset):
    list = [count + 1 for count, ele in enumerate(dataset) if ele <= float(enteredtime)]
    x = 0
    for data in list:
        x = data
    return x
