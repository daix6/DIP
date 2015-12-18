#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse
from utils import *
from filter2d import *

def main():
  # Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', type=str, default='task_1.png', help='The path of the image that you want to deal with.')
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

  # 2-1 filter
  task_1 = open_image(filename)
  task_1_arithmetic_mean_3x3 = arithmetic_mean_filter(task_1, (3,3))
  save_image(task_1_arithmetic_mean_3x3, 'arithmetic_mean_3x3.png')

  task_1_arithmetic_mean_9x9 = arithmetic_mean_filter(task_1, (9,9))
  save_image(task_1_arithmetic_mean_9x9, 'arithmetic_mean_9x9.png')

  task_1_harmonic_mean_3x3 = harmonic_mean_filter(task_1, (3,3))
  save_image(task_1_harmonic_mean_3x3, 'task_1_harmonic_mean_3x3.png')

  task_1_harmonic_mean_9x9 = harmonic_mean_filter(task_1, (9,9))
  save_image(task_1_harmonic_mean_9x9, 'task_1_harmonic_mean_9x9.png')

  task_1_contra_harmonic_mean_3x3 = contra_harmonic_mean_filter(task_1, (3,3), -1.5)
  save_image(task_1_contra_harmonic_mean_3x3, 'task_1_contra_harmonic_mean_3x3.png')

  task_1_contra_harmonic_mean_9x9 = contra_harmonic_mean_filter(task_1, (9,9), -1.5)
  save_image(task_1_contra_harmonic_mean_9x9, 'task_1_contra_harmonic_mean_9x9.png')


if __name__ == '__main__':
  main()