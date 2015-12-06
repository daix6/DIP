#!/usr/env/bin python
# -*- coding: utf-8 -*-

# Reference: http://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/

from utils import *
from dft2d import dft1d

def fft1d(data, flags):
  N = len(data)

  if N <= 32:
    return dft1d(data, 1)
  else:
    even = fft1d(data[::2], flags)
    odd = fft1d(data[1::2], flags)
    factor = np.exp(-2j * np.pi * np.arange(N)) if flags == 1 \
        else np.exp(-2j * np.pi * np.arange(N) / N)
    return np.concatenate((even + factor[:N / 2] * odd,
                          even + factor[N / 2:] * odd))

@ffting
def fft2d(input_img, flags):
  ''' Fast Discrete fourier transform, returns a 2d matrix

  input_img: PIL.Image.Image. To handle.
  flags: 1 for fft, -1 for ifft
  '''
  if not flags in [1, -1]:
    raise Exception("Wrong flags, it should be 1 or -1.")

  data = np.reshape(input_img.getdata(), input_img.size[::-1])

  # Because fft only supports 2's pow
  new = pad_to_2spow(data)

  fft_row = np.apply_along_axis(fft1d, 1, new, [flags]) # For each row
  result = np.apply_along_axis(fft1d, 0, fft_row, [flags]) # For each column

  return result
