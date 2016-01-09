#!/usr/env/bin python
# -*- coding: utf-8 -*-

import numpy as np

def main():
  r = open('./result.txt', 'r')
  data = np.array(r.readlines()).reshape((21, 5, 3))
  r.close()

  r = open('./result.out', 'w')
  r.write('CASE & \\multicolumn{2}{|c|}{SSD} & \\multicolumn{2}{|c|}{NCC} & \\multicolumn{2}{|c|}{ASW} & \\multicolumn{2}{|c|}{SSD_10} & \\multicolumn{2}{|c|}{NCC_10} \\\\ \\hline\n')
  for case in data:
    s = ''
    name = case[0][0][case[0][0].index('-')+2:case[0][0].index(',')] + ' & '
    s+= name
    for (index,test) in enumerate(case):
      left = test[1][:5]
      right = test[1][test[1].index(' ')+1:test[1].index(' ')+6]
      s += left + ' & ' + right + ' & ' if index != 4 else left + ' & ' + right

    s += ' \\\\ \\hline\n'

    r.write(s)

  r.close()

if __name__ == '__main__':
  main()