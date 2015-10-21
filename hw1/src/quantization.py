#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from math import floor
from bisect import bisect_right

def quantize(input_img, level):
  if level > 255 or level < 0:
    raise Exception("wrong level")

  in_level = len(input_img.getcolors())

  in_width, in_height = input_img.size

  out_palette = [255 * p / (level-1) for p in range(level)]
  out_pixels = []
  for y in range(in_height):
    row = []
    for x in range(in_width):
      p = input_img.getpixel((x, y))
      i = bisect_right(out_palette, p)
      if i == len(out_palette):
        out_p = out_palette[i-1]
      elif out_palette[i] - p < p - out_palette[i-1]:
        out_p = out_palette[i]
      else:
        out_p = out_palette[i-1]
      row.append(out_p)
    out_pixels.append(row)

  out = Image.new(input_img.mode, input_img.size)
  for y in range(in_height):
    for x in range(in_width):
      out.putpixel((x,y), out_pixels[y][x])

  return out
