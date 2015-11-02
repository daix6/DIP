#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

from histogram import plot_hist, equalize_hist

def test_plot_hist(filename, dist):
  im = Image.open(filename)
  plot_hist(im, os.path.join(dist, 'hist.png'))

def test_equalize_hist(filename, dist):
  im = Image.open(filename)
  result = equalize_hist(im)
  out_path = os.path.join(dist, 'equalized.png')
  result.save(out_path)
  print 'The equalized image has been saved to %s.' % out_path
  # new histogram
  plot_hist(im, os.path.join(dist, 'equalized_hist.png'))

def main():
  # get path
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist')
  filename = os.path.join(parent_dir, 'assets', '43.png')

  # test
  print '1. test plot histogram'
  test_plot_hist(filename, dist_dir)
  print ''
  print '2. test histogram equalization'
  test_equalize_hist(filename, dist_dir)

if __name__ == '__main__':
  main()
