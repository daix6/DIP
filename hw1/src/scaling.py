#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from scipy import interpolate

import os
import math
import numpy

def scale(input_img, size):
  # basic infomation
  in_size = input_img.size
  in_width, in_height = in_size
  out_width, out_height = size

  # compute the ratio
  width_ratio = float(in_width) / out_width
  height_ratio = float(in_height) / out_height

  # x: right, y: down  
  x = numpy.arange(0.0, in_width, width_ratio)
  y = numpy.arange(0.0, in_height, height_ratio)

  in_pixels = []
  for in_y in range(in_height):
    row = []
    for in_x in range(in_width):
      row.append(input_img.getpixel((in_x, in_y)))
    in_pixels.append(row)

  interpolation = interpolate.RectBivariateSpline(\
    numpy.arange(in_height), # y
    numpy.arange(in_width),  # x
    numpy.array(in_pixels)  # original pixels
  )

  pixels = interpolation(y, x) # __call__(x, y)

  return createImage(input_img.mode, size, pixels)

# Without scipy version
def scaling(input_img, size):
  """ Scaling the given picture with Nearest Neighbor Interpolation algorithm.
  input_img Image
  size      tuple
  """
  # basic infomation
  in_size = input_img.size
  in_width, in_height = in_size
  out_width, out_height = size

  # compute the ratio
  width_ratio = float(in_width) / out_width
  height_ratio = float(in_height) / out_height

  out_pixels = []

  # x: right, y: down  
  for out_y in range(out_height):
    row = []
    for out_x in range(out_width):
      # get corresponding coordinate of output from input
      in_x = round(out_x * width_ratio)
      in_y = round(out_y * height_ratio)
      row.append(input_img.getpixel((in_x, in_y)))
    out_pixels.append(row)

  """ Bilinear Interpolation
  for out_y in range(out_height):
    row = []
    for out_x in range(out_width):
      # get corresponding coordinate of output from input
      temp_x = out_x * width_ratio
      temp_y = out_y * height_ratio
      i = math.floor(temp_x)
      j = math.floor(temp_y)
      u = temp_x - i
      v = temp_y - j

      # avoid overflow
      if (i+1>=in_width):
        i = in_width-2
      if (j+1>=in_height):
        j = in_height-2

      color = (1-u)*(1-v)*input_img.getpixel((i, j)) + \
              (1-u)*v*input_img.getpixel((i, j+1)) + \
              u*(1-v)*input_img.getpixel((i+1, j)) + \
              u*v*input_img.getpixel((i+1, j+1))

      row.append(int(color))
  """
  return createImage(input_img.mode, size, out_pixels)


def createImage(mode, size, pixels):
  """ Create an Image Object
  mode   string
  size   tuple
  pixels list
  """
  out = Image.new(mode, size)

  for y in range(size[1]):
    for x in range(size[0]):
      out.putpixel((x,y), int(pixels[y][x]))

  return out
