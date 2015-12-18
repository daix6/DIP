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
  image_data = np.array(image.getdata(), dtype=np.float64).reshape(image.size[::-1])
  return image_data