#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_hist(input_img, dist):
    '''
    Plot the histogram of input_img (Image) by making use of matplotlib.
    '''
    # get the number of each intensity value
    data = np.array(input_img.getdata())
    plt.xlabel('Pixel Intensity Value')
    plt.ylabel('Number of pixels')
    plt.xlim((0, 256))
    plt.hist(data, 256, color='black')
    plt.savefig(dist)
    print 'Histogram has been save to {0}.'.format(dist)

def equalize_hist(input_img):
    '''
    Histogram equalization.
    '''
    size = input_img.width * input_img.height

    colors = input_img.getcolors()
    if len(colors) != 256:
        # fill the missing part with 0
        map(lambda i: colors.insert(i, (0, i)) if colors[i][1] != i else None, range(256))

    # compute cumulative distribution
    cdf = [sum(map(lambda x: x[0], colors[0:(value+1)])) for (count, value) in colors]
    # according cdf to update the pallate
    hist = [round((cdf[i] * 1.0/size)*255) for i in range(256)]

    return Image.eval(input_img, lambda x: hist[x])