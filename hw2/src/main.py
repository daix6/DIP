#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

from histogram import plot_hist, equalize_hist
from filter import filter2d, smooth, laplacian, origin, high_boost

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
  plot_hist(result, os.path.join(dist, 'equalized_hist.png'))

def test_smooth_filter(filename, dist):
  im = Image.open(filename)

  sizes = [(3, 3), (7, 7), (11, 11)]
  for size in sizes:
    result = smooth(im, size)
    out_name = 'smooth-%d-%d.png' % size
    out_path = os.path.join(dist, out_name)
    result.save(out_path)
    print 'The smooth {0} result has been save to {1}.'.format(size, out_path)

def test_laplacian_filter(filename, dist):
  im = Image.open(filename)

  result = filter2d(im, laplacian + origin)
  out_name = 'laplacian.png'
  out_path = os.path.join(dist, out_name)
  result.save(out_path)
  print 'The laplacian filter result has been save to {0}.'.format(out_path)

def test_high_boost(filename, dist):
  im = Image.open(filename)

  ks = [.5, 1., 1.5, 2.5, 5.]
  for k in ks:
    result = high_boost(im, k)
    out_name = 'high-boost-{0}.png'.format(k)
    out_path = os.path.join(dist, out_name)
    result.save(out_path)
    print 'The high boost filter result has been saved to {0}.'.format(out_path)

def main():
  # get path
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist')
  filename = os.path.join(parent_dir, 'assets', '43.png')

  # test
  print '1. test plot histogram.'
  test_plot_hist(filename, dist_dir)
  
  print '\n2. test histogram equalization.'
  test_equalize_hist(filename, dist_dir)

  print '\n3. test smooth filter.'
  test_smooth_filter(filename, dist_dir)

  print '\n4. test laplacian filter.'
  test_laplacian_filter(filename, dist_dir)

  print '\n5. test high boosting filter.'
  test_high_boost(filename, dist_dir)

if __name__ == '__main__':
  main()
