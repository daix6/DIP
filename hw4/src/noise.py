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

class SaltPepperGenerator(object):
  def __init__(self, level, ps, pp):
    self.level = level
    self.ps = ps
    self.pp = pp

  def salt(self, origin):
    return self.level - 1 if np.random.random_sample() < self.ps else origin

  def pepper(self, origin):
    return 0 if np.random.random_sample() < self.pp else origin

  def sp(self, origin):
    rs = np.random.random_sample()

    if rs < self.ps:
      return self.level - 1
    elif rs > (1 - self.pp):
      return 0
    else:
      return origin

  def generator(self, origin):
    return self.sp(origin)
          

def add_gaussian(data, mu, sigma, mode='L'):
  generator = GaussianGenerator(mu, sigma)

  def add_noise(p):
    return p + generator.generator()

  vfunc = np.vectorize(add_noise)

  if mode in 'RGBA':
    rgb = vfunc(data[:3])
    alpha = data[3] if len('RGBA') == 4 else np.array([])
    return np.concatenate((rgb, [alpha])) if alpha.size else rgb

  return vfunc(data)

def add_salt_pepper(data, level=256, ps=0.0, pp=0.0, mode='L'):
  generator = SaltPepperGenerator(level, ps, pp)

  def add_noise(p):
    return generator.generator(p)

  vfunc = np.vectorize(add_noise)

  if mode in 'RGBA':
    rgb = vfunc(data[:3])
    alpha = data[3] if len('RGBA') == 4 else np.array([])
    return np.concatenate((rgb, [alpha])) if alpha.size else rgb

  return vfunc(data)