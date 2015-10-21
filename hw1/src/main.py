#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

from scaling import scale
from quantization import quantize

def test_scale(filename, dist):
  im = Image.open(filename)

  # different cases from given problems
  expections = []
  expections.append([(192, 128), (96, 64), (48, 32), (24, 16), (12, 8)]) # 1.
  expections.append([(300, 200)]) # 2.
  expections.append([(450, 300)]) # 3.
  expections.append([(500, 200)]) # 4.

  for case in expections:
    print "Scaling case %d" % expections.index(case)

    for size in case:
      out = scale(im, size)

      out_name = "scaling-%dx%d.png" % out.size
      out_path = os.path.join(dist, out_name)
      out.save(out_path)
      print "    Picture %s has been saved to the assets folder !" % out_name

def test_quantize(filename, dist):
  im = Image.open(filename)

  # different cases
  expections = [128, 32, 8, 4, 2]

  print "Quantiztion"
  for level in expections:
    out = quantize(im, level)

    out_name = "quantization-%d.png" % level
    out_path = os.path.join(dist, out_name)
    out.save(out_path)
    print "    Picture %s has been saved to the assets folder !" % out_name

def main():
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist')
  filename = os.path.join(parent_dir, 'assets', '43.png')

  test_scale(filename, dist_dir)
  print ""
  test_quantize(filename, dist_dir)

if __name__ == '__main__':
  main()
