#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse
from utils import *
from filter2d import *

def main():
  # Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', type=int, choices=[1,2,3], help='The task you want to run: 1, 2 or 3.')
  parser.add_argument('-s', type=str, default='43.png', help='The path of the image that you want to deal with.')
  args = parser.parse_args()

  # Path
  file_dir = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.split(file_dir)[0]
  dist_dir = os.path.join(parent_dir, 'dist')

  if args.t == 1:
    filename = os.path.join(parent_dir, 'assets', 'task_1.png')
  elif args.t == 2:
    filename = os.path.join(parent_dir, 'assets', 'task_2.png')
  else:
    filename = os.path.join(parent_dir, 'assets', 'task_3', args.s)

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

  if args.t == 1:
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

  elif args.t == 2:
    task_2 = open_image(filename)
    task_2_gauss = add_guassian(task_2, 0.0, 40.0)
    save_image(task_2_gauss, 'task_2_guass_0_40.png')

if __name__ == '__main__':
  main()