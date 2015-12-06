#!/usr/env/bin python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

#- Decorator, for console info.
def dfting(func):
  def wrapper(*args, **kwargs):
    print 'Begin to 2d Discrete Fourier Transform.'
    data = func(*args, **kwargs)
    print 'Finish 2d Discrete Fourier Transforming.'
    return data
  return wrapper

def ffting(func):
  def wrapper(*args, **kwargs):
    print 'Begin to 2d Fast Discrete Fourier Transform.'
    data = func(*args, **kwargs)
    print 'Finish 2d Fast Discrete Fourier Transforming.'
    return data
  return wrapper

def saving(func):
  def wrapper(*args, **kwargs):
    print '  Begin to saving image.'
    func(*args, **kwargs)
    print '  Finish saving ' + args[1] + '.'
  return wrapper

#- Helper
def shift(data):
  ''' Shift the result of dft to centralize the frequency spectrum.
  data: an 2d matrix
  '''
  shape = data.shape
  for axis, size in enumerate(shape):
    mid = (size + 1) / 2
    opposite = np.concatenate((np.arange(mid, size), np.arange(mid)))
    data = np.take(data, opposite, axis=axis)
  return data

def scaling(data, L=256):
  ''' Scaling the data to [0, L)
  data: an 2d matrix
  '''
  positive = data - np.min(data) # negative to positive
  intensity = (L - 1) * (positive / np.max(positive)) # minify to [0, L-1]
  return np.uint8(intensity) # to int

def pad_to_2spow(data):
  M, N = data.shape

  to_m, to_n = 2 ** np.ceil(np.log2(data.shape))

  zeros = np.zeros((to_m, to_n))
  zeros[:M, :N] = data

  return zeros