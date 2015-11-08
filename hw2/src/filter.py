#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

import numpy as np

def filter2d(input_img, filter):
    '''
    Filter input_img (Image) with given filter.
    Handle every pixel and compute SOP.
    '''
    w, h = input_img.size
    m, n = len(filter), len(filter[0])
    padding_x, padding_y = m/2, n/2 # floor
    # get all pixels
    pixels = [[input_img.getpixel((x,y)) for x in range(w)] for y in range(h)]

    out_pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            # mat = np.zeros((m, n))
            # Use intensity value at (x, y) to avoid edge be black when use zeros to fill.
            mat = np.full((m, n), pixels[y][x], dtype=np.int)
            for xx in range(x - padding_x, x + padding_x + 1):
                for yy in range(y - padding_y, y + padding_y + 1):
                    if xx >=0 and xx < w and yy >= 0 and yy < h:
                        # Fill the mat
                        mat[xx - x + padding_x][yy - y + padding_y] = pixels[yy][xx]
            # convert from 2-d to 1-d and then product and sum
            row.append(np.dot(filter.flatten(), mat.flatten()))
        out_pixels.append(row)

    out = Image.new(input_img.mode, input_img.size)
    for y in range(h):
        for x in range(w):
            out.putpixel((x,y), int(out_pixels[y][x]))

    return out

def smooth(input_img, size):
    '''
    Smooth filtering the input_img (Image).
    The elements in size (tuple) must be odd to construct a matrix.
    '''

    m, n = size
    # use filter [[1,1,1], *size]
    return filter2d(input_img, np.full((m, n), float(1) / (m*n)))

def high_boost(input_img, k = 1):
    '''
    Filter the input_img (Image) with high_boost method.
    
    Formula:
        g(x,y) = f(x,y) + k*g_{mask}(x,y)
        g_{mask}(x,y) = f(x,y) - \hat{f}(x,y)
    '''
    w, h = input_img.size

    blur = smooth(input_img, (3, 3))

    out_pixels = [[input_img.getpixel((x, y)) + \
      float(k) * (input_img.getpixel((x, y)) - \
      blur.getpixel((x, y))) for x in range(w)] for y in range(h)]

    out = Image.new(input_img.mode, input_img.size)
    for y in range(h):
        for x in range(w):
            out.putpixel((x,y), int(out_pixels[y][x]))

    return out

laplacian = np.array([[1, 1, 1],
            [1, -8, 1],
            [1, 1, 1]])

origin = np.array([[0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]])