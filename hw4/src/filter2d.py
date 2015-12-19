#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def filter2d(data, filter, geometric=False):
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

def arithmetic_mean_filter(data, size, mode='L'):
  if mode in 'RGBA':
    return [arithmetic_mean_filter(channel, size) for channel in data]

  m, n = size
  filter = np.full(size, float(1) / (m * n))

  return filter2d(data, filter)

def harmonic_mean_filter(data, size, mode='L'):
  if mode in 'RGBA':
    return [harmonic_mean_filter(channel, size) for channel in data]

  reciprocal = np.reciprocal(data)
  result = np.reciprocal(arithmetic_mean_filter(reciprocal, size))

  return result

def contra_harmonic_mean_filter(data, size, q, mode='L'):
  if mode in 'RGBA':
    return [contra_harmonic_mean_filter(channel, size, q) for channel in data]

  numerator = np.power(data, q+1)
  denominator = np.power(data, q)
  filter = np.full(size, float(1))
  result = filter2d(numerator, filter) / filter2d(denominator, filter)

  return result

def geometric_mean_filter(data, size, mode='L'):
  if mode in 'RGBA':
    return [geometric_mean_filter(channel, size) for channel in data]

  M, N = data.shape
  m, n = size
  pad_x, pad_y = m/2, n/2

  def product(x, y):
    neighbors = np.full((m,n), data[x, y])
    for i in range(x - pad_x, x + pad_x + 1):
      for j in range(y - pad_y, y + pad_y + 1):
        if i >= 0 and j >= 0 and i < M and j < N:
          neighbors[i - x + pad_x, j - y + pad_y] = data[i, j]

    return np.prod(np.power(neighbors, float(1) / (m * n)))

  w, h = np.meshgrid(range(M), range(N), indexing='ij')
  vfunc = np.vectorize(product)
  return vfunc(w, h)

def statistic_filter(data, size, percent, mode='L'):
  if percent < 0 or percent > 100:
    return ValueError('Wrong percent, it should between [0, 100]')

  if mode in 'RGBA':
    return [statistic_filter(channel, size, percent) for channel in data]

  M, N = data.shape
  m, n = size
  pad_x, pad_y = m/2, n/2

  def get(x, y):
    neighbors = []
    for i in range(x - pad_x, x + pad_x + 1):
      for j in range(y - pad_y, y + pad_y + 1):
        if i >= 0 and j >= 0 and i < M and j < N:
          neighbors.append(data[i, j])

    # https://github.com/numpy/numpy/blob/master/numpy/lib/function_base.py#L3494
    neighbors.sort()
    index = percent / 100.0 * (len(neighbors) - 1)
    index_below, index_above = int(np.floor(index)), int(np.ceil(index))

    return (neighbors[index_below] + neighbors[index_above]) / 2.0

  w, h = np.meshgrid(range(M), range(N), indexing='ij')
  vfunc = np.vectorize(get)
  return vfunc(w, h)