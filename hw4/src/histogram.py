#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import takewhile
from utils import *

def equalize(data, level=256, mode='L'):
  if mode in 'RGBA':
    rgb = [equalize(channel) for channel in data[:3]]
    alpha = data[3] if len(mode) == 4 else np.array([])
    return np.concatenate((rgb, [alpha])) if alpha.size else rgb

  size = data.shape[0] * data.shape[1]
  # http://stackoverflow.com/questions/10741346/numpy-most-efficient-frequency-counts-for-unique-values-in-an-array
  color, count = np.unique(data, return_counts=True)
  colors = zip(color, count)
  colors.sort(key=lambda x: x[0])

  pdf = [(c[0], c[1] / float(size)) for c in colors]
  cdf = [sum(x[1] for x in takewhile(lambda p: p[0] <= i, pdf))
          for i in range(level)]

  return [round(float(i) * (level - 1)) for i in cdf]

def equalize_together(data, level=256, mode='RGB'):
  '''
  Only handle 'RGB' or 'RGBA', ignore Alpha channel.
  '''
  if not mode in 'RGBA':
    raise Exception('Wrong data.')

  vector = np.dstack(data[:3])
  size = vector.shape[0] * vector.shape[1] * vector.shape[2]

  color, count = np.unique(vector, return_counts=True)
  colors = zip(color, count)
  colors.sort(key=lambda x: x[0])

  pdf = [(c[0], c[1] / float(size)) for c in colors]
  cdf = [sum(x[1] for x in takewhile(lambda p: p[0] <= i, pdf)) for i in range(level)]
  return [round(float(i) * (level - 1)) for i in cdf]

def equalize_hist(data, level=256, mode='L', way='seperate'):
  if not way in ['seperate', 'together']:
    raise Exception('Wrong way to caculate histogram')

  if way == 'together':
    lookup = equalize_together(data, level, mode)
    return replace(data, lookup)

  lookup = equalize(data, level, mode)

  if mode in 'RGBA':
    rgb = [replace(d, l) for (d, l) in zip(data[:3], lookup)]
    alpha = data[3] if len(mode) == 4 else np.array([])
    return np.concatenate((rgb, [alpha])) if alpha.size else rgb

  return replace(data, lookup)

# Works like Image.eval, replace every element with specified value
def replace(data, lookup):
  r = np.copy(data)
  indexs = [zip(*np.where(r == index)) for (index,value) in enumerate(lookup)]

  for (idx, v) in enumerate(indexs):
    for i in v:
      r[i] = lookup[idx]

  return r
