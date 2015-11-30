#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from PIL import Image
from scipy.misc import lena
from matplotlib import pyplot as plt

def main():
  img = lena()
  h, w = img.shape

  out_img = np.zeros((h,w), np.complex)

  for v in range(h):
    for u in range(w):
      s = complex(0)
      for y in range(h):
        for x in range(w):
          s += img[y,x] * np.exp(-2j * np.pi * (u*x/w + v*y/h))

      out_img[u, v] = s
  
  plt.imshow(out_img, cmap='gray')
  plt.show()
  
if __name__ == '__main__':
  main()
