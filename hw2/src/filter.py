#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

import numpy as np

def filter2d(input_img, filter):
    w, h = input_img.size
    m, n = len(filter), len(filter[0])
    padding_x, padding_y = m/2, n/2
    pixels = [[input_img.getpixel((x,y)) for x in range(w)] for y in range(h)]

    out_pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            # mat = np.zeros((m, n))
            mat = np.full((m, n), pixels[y][x]) # future warning
            for xx in range(x - padding_x, x + padding_x + 1):
                for yy in range(y - padding_y, y + padding_y + 1):
                    if xx >=0 and xx < w and yy >= 0 and yy < h:
                        mat[xx - x + padding_x][yy - y + padding_y] = pixels[yy][xx]
            row.append(np.dot(filter.flatten(), mat.flatten()))
        out_pixels.append(row)

    out = Image.new(input_img.mode, input_img.size)
    for y in range(h):
        for x in range(w):
            out.putpixel((x,y), int(out_pixels[y][x]))

    return out

def smooth(input_img, size):
    m, n = size
    return filter2d(input_img, np.full((m, n), float(1) / (m*n)))
