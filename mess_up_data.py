import numpy as np

def addNoise(intensity, std):
    # adding noise
    noisy_intensity = intensity + np.random.normal(0, std)

    # limiting between 0 and 100
    if noisy_intensity > 100:
        noisy_intensity = 100
    
    if noisy_intensity < 0:
        noisy_intensity = 0

    return noisy_intensity


def nextGap(duration, frequency):
    next_dur = abs(np.random.normal(duration, duration/2))
    next_time = abs(np.random.normal(frequency, frequency/2))
    
    return next_dur, next_time
