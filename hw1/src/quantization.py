#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from math import floor
from bisect import bisect_right

def quantize(input_img, level):
  in_level = len(input_img.getcolors())
  in_width, in_height = input_img.size

  # the corresponding palette
  out_palette = [255 * p / (level-1) for p in range(level)]
  out_pixels = []

  # get pixels
  for y in range(in_height):
    row = []
    for x in range(in_width):
      p = input_img.getpixel((x, y))
      # find the corresponding pixel in 255 level
      i = bisect_right(out_palette, p)
      if i == len(out_palette) or out_palette[i] - p > p - out_palette[i-1]:
        out_p = out_palette[i-1]
      else:
        out_p = out_palette[i]
      row.append(out_p)
    out_pixels.append(row)

  # create new image
  out = Image.new(input_img.mode, input_img.size)
  for y in range(in_height):
    for x in range(in_width):
      out.putpixel((x,y), out_pixels[y][x])

  return out
