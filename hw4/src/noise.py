#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ref: https://en.wikipedia.org/wiki/Normal_distribution#Generating_values_from_normal_distribution
#      http://www.design.caltech.edu/erik/Misc/Gaussian.html
#      https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform

from utils import *

class GaussianGenerator(object):
  def __init__(self, mu, sigma):
    self.generate = True
    self.mu = mu
    self.sigma = sigma
    self.cache = None

  def generator(self):
    if (not self.generate):
      self.generate = not self.generate
      return self.cache * self.sigma + self.mu

    self.generate = not self.generate

    u = np.random.random_sample()
    v = np.random.random_sample()

    r = np.sqrt(-2 * np.log(v))
    theta = 2 * np.pi * u

    z = r * np.cos(theta)
    self.cache = r * np.sin(theta)

    return z * self.sigma + self.mu

  def generator_polar(self):
    if (not self.generate):
      self.generate = not self.generate
      return self.cache * self.sigma + self.mu

    self.generate = not self.generate

    # between (-1,1)
    u = 2 * np.random.random_sample() - 1
    v = 2 * np.random.random_sample() - 1

    s = u*u + v*v
    r = sqrt((-2 * np.log(s)) / s)

    z = u * r
    self.cache = v * r

    return z

def add_gaussian(data, mu, sigma):
  generator = GaussianGenerator(mu, sigma)

  def add_noise(p):
    return p + generator.generator()

  vfunc = np.vectorize(add_noise)
  return vfunc(data)