#!/usr/env/bin python
# -*- coding: utf-8 -*-

from utils import *
from dft2d import dft, idft

smooth = np.full((7, 7), 1.0/ (7 * 7))

# laplacian = np.array([[1, 1, 1],
#                       [1, -8, 1],
#                       [1, 1, 1]])

# laplacian = np.array([[0, 1, 0],
#                      [1, -4, 1],
#                      [0, 1, 0]])

laplacian = np.array([[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]])

# laplacian = np.array([[0, -1, 0],
#                      [-1, 4, -1],
#                      [0, -1, 0]])

origin = np.array([[0, 0, 0],
                  [0, 1, 0],
                  [0, 0, 0]])

def filter2d_freq(input_img, filter):
  ''' Filter an image in frequency domain.
  input_img, an instance of PIL.Image.Image
  filter, an 2d array
  '''
  data = np.reshape(input_img.getdata(), input_img.size[::-1])
  filter_ = np.asarray(filter)

  M, N = data.shape
  m, n = filter_.shape

  # padding to avoid black edge.
  padding = np.pad(data, (m, n), 'edge')
  pM, pN = padding.shape # pM = M + 2*m, pN = N + 2*n

  P, Q = pM + m - 1, pN + n - 1

  f, h = np.zeros((P, Q)), np.zeros((P, Q))
  f[:pM, :pN], h[:m, :n] = padding, filter_

  F, H = dft(f), dft(h)

  return idft(F * H).real[m:m+M, n:n+N]
