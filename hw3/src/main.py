#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse
from utils import *

from dft2d import dft2d
from filter import *
from fft2d import fft2d

def main():
  # Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', type=str, default='43.png', help='The path of the image that you want to deal with.')
  args = parser.parse_args()

  # Path
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist')
  filename = os.path.join(parent_dir, 'assets', args.s)

  if not os.path.exists(filename):
    raise Exception("There is no file named " + filename + ".")

  if not os.path.exists(dist_dir):
    raise Exception("There is no folder named " + dist_dir + ".")

  # Helper
  @saving
  def save_image(data, name, dist=dist_dir):
    ''' Save image as dist/name.
    data: A 2d matrix
    '''
    if len(data.shape) != 2:
      raise Exception("Wrong data when saving file")

    Image.fromarray(data).convert('L').save(os.path.join(dist, name))

  image = Image.open(filename)

  # DFT
  image_dft = dft2d(image, 1)
  image_dft_shift = shift(image_dft) # Centralize
  image_dft_scaling = scaling(np.log(1 + np.abs(image_dft_shift))) # 1 for avoid ln(0)
  save_image(image_dft_scaling, 'dft-spectrum.png')

  # IDFT
  save_image(dft2d(image_dft, -1).real, 'idft-dft.png')

  ## Filter
  # Smooth with 7x7
  image_smooth = filter2d_freq(image, smooth)
  save_image(image_smooth, 'smooth-7x7.png')

  image_sharp = filter2d_freq(image, laplacian)
  save_image(image_sharp, 'sharp-laplacian.png')

  image_plus_sharp = filter2d_freq(image, laplacian + origin)
  save_image(image_plus_sharp, 'origin-with-edge.png')

  # FFT
  image_fft = fft2d(image, 1)
  image_fft_shift = shift(image_fft)
  image_fft_scaling = scaling(np.log(1 + np.abs(image_fft_shift)))
  save_image(image_fft_scaling, 'fft-spectrum.png')

  # IFFT
  save_image(dft2d(image_fft, -1).real, 'ifft-fft.png')

if __name__ == '__main__':
  main()