#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_hist(input_img, dist):
    data = np.array(input_img.getdata())
    plt.xlabel('Pixel Intensity Value')
    plt.ylabel('Number of pixels')
    plt.xlim((0, 256))
    plt.hist(data, 256, color='black')
    plt.savefig(dist)
    print "Histogram has been save to %s." % dist

def equalize_hist(input_img):
    size = input_img.width * input_img.height

    colors = input_img.getcolors()
    if len(colors) != 256:
        map(lambda i: colors.insert(i, (0, i)) if colors[i][1] != i else None, range(256))

    cdf = [sum(map(lambda x: x[0], colors[0:(value+1)])) for (count, value) in colors]
    hist = [round((cdf[i] * 1.0/size)*255) for i in range(256)]

    return Image.eval(input_img, lambda x: hist[x])