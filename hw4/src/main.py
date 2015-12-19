#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse
from utils import *

from filter2d import *
from noise import *

def main():
  # Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', type=int, choices=[1,2,3], required=True, help='The task you want to run: 1, 2 or 3.')
  parser.add_argument('-s', type=str, default='43.png', help='The path of the image that you want to deal with.')
  args = parser.parse_args()

  # Path
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist', 'task_%d' % args.t)

  if args.t == 1:
    filename = os.path.join(parent_dir, 'assets', 'task_1.png')
  elif args.t == 2:
    filename = os.path.join(parent_dir, 'assets', 'task_2.png')
  else:
    filename = os.path.join(parent_dir, 'assets', 'task_3', args.s)

  if not os.path.exists(filename):
    raise Exception("There is no file named " + filename + ".")

  if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

  # Helper
  @saving
  def save_image(data, name, mode='L', dist=dist_dir):

    if mode == 'L':
      Image.fromarray(data).convert(mode).save(os.path.join(dist, name))
    elif mode in 'RGBA':
      merged = [Image.fromarray(channel).convert('L') for channel in data]
      Image.merge(mode, merged).save(os.path.join(dist, name))
    else:
      raise Exception('Invalid image mode %s.' % mode)

  if args.t == 1:
    # 2-1 filter
    task_1, mode = open_image(filename)

    sizes = [(3,3), (9,9)]
    # 2-1-1
    for s in sizes:
      r = arithmetic_mean_filter(task_1, s)
      save_image(r, 'arithmetic_mean_%dx%d.png' % s, mode)

    # 2-1-2
    for s in sizes:
      r = harmonic_mean_filter(task_1, s)
      save_image(r, 'harmonic_mean_%dx%d.png' % s, mode)

    # 2-1-3
    for s in sizes:
      r = contra_harmonic_mean_filter(task_1, s, -1.5)
      save_image(r, 'contra_harmonic_mean_%dx%d.png' % s, mode)

  elif args.t == 2:
    task_2, mode = open_image(filename)

    # 2-2-2
    gauss = add_gaussian(task_2, 0.0, 40.0)
    save_image(gauss, 'guass_0_40.png', mode)

    gauss_amf = arithmetic_mean_filter(gauss, (3,3), mode)
    save_image(gauss_amf, 'guass_arithmetic.png', mode)

    gauss_gmf = geometric_mean_filter(gauss, (3,3), mode)
    save_image(gauss_gmf, 'gauss_geometric.png', mode)

    gauss_median = statistic_filter(gauss, (3,3), 50, mode)
    save_image(gauss_median, 'gauss_median.png', mode)

if __name__ == '__main__':
  main()