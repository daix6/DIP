#!/usr/env/bin python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

# Decorator for information
def saving(func):
  def wrapper(*args, **kwargs):
    print '  Begin to saving image.'
    func(*args, **kwargs)
    print '  Finish saving ' + args[1] + '.'
  return wrapper

# Helper
def open_image(path):
  image = Image.open(path)
  return (image_to_array(image), image.mode)

def image_to_array(image):
  mode = image.mode

  if mode == 'L':
    image_data = np.array(image.getdata(), dtype=np.float64).reshape(image.size[::-1])
  elif mode in 'RGBA':
    image_data = [image_to_array(channel) for channel in image.split()]
  else:
    raise Exception('Can\'t hanldle the image type %s yet.' % mode)

  return image_data