#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def filter2d(data, filter):
    '''
    data: 2d pixel matrix
    filter: 2d matrix or array or something else
    '''
    M, N = data.shape
    m, n = len(filter), len(filter[0])
    pad_x, pad_y = m/2, n/2

    # http://stackoverflow.com/questions/28930465/what-is-the-difference-between-flatten-and-ravel-functions-in-numpy
    right = filter.ravel() if isinstance(filter, np.ndarray) else np.array(filter).ravel()

    def correlation(x, y):
      left = np.full((m,n), data[x, y])
      for i in range(x - pad_x, x + pad_x + 1):
        for j in range(y - pad_y, y + pad_y + 1):
          if i >= 0 and j >= 0 and i < M and j < N:
            left[i - x + pad_x, j - y + pad_y] = data[i, j]

      return np.dot(left.ravel(), right)

    w, h = np.meshgrid(range(M), range(N), indexing='ij')
    vfunc = np.vectorize(correlation)
    return vfunc(w, h)

def arithmetic_mean_filter(data, size):
  m, n = size
  filter = np.full(size, float(1) / (m * n))

  return filter2d(data, filter)

def harmonic_mean_filter(data, size):
  reciprocal = np.reciprocal(data)
  result = np.reciprocal(arithmetic_mean_filter(reciprocal, size))
  
  return result

def contra_harmonic_mean_filter(data, size, q):
  numerator = np.power(data, q+1)
  denominator = np.power(data, q)
  filter = np.full(size, float(1))
  result = filter2d(numerator, filter) / filter2d(denominator, filter)

  return result
