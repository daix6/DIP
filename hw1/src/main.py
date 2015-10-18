#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image

from scaling import scale

dist = "../dist/"

def test_scale(filename):
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

def main():
  test_scale("../assets/43.png")

if __name__ == '__main__':
  main()
