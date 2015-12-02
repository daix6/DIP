#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

def matrix(n, flags):
  ''' The dft matrix with size n x n.
  flags: 1 for dft, -1 for idft
  '''
  W = np.asmatrix(np.arange(n))
  return np.exp((flags * -2j * np.pi / n) * W.T * W)

def dft(data):
  '''
  data: The pixel values of pic in 2d matrix form.
  '''
  M, N = data.shape # M for rows' length, N for col length
  return np.asarray(matrix(M, 1) * data * matrix(N, 1))

def idft(data):
  '''
  data: The pixel values of pic in 2d matrix form.
  '''
  M, N = data.shape # M for rows' length, N for col length
  return np.asarray((matrix(M, -1) * data * matrix(N, -1))/ (M*N))

def dft2d(input_img, flags):
  ''' Discrete fourier transform, returns a 2d matrix
  input_img: PIL.Image.Image. To handle.
  flags: 1 for dft, -1 for idft
  '''
  if not isinstance(input_img, Image.Image):
    raise Exception("Wrong image, it should be an instance of PIL.Image.Image.")
  if not flags in [1, -1]:
    raise Exception("Wrong flags, it should be 1 or -1.")

  data = np.reshape(input_img.getdata(), input_img.size[::-1])
  return dft(data) if flags == 1 else idft(data)

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
