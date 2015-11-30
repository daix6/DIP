#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import arctan, tan, array
from math import floor, sqrt, pi
from PIL import Image
import cv2

import sys

def cylindrical_projection(img):
    # cylindrical projection
    w, h = img.size
    hfOV = pi / 4

    f = float(w) / (2 * tan(hfOV / 2))

    new_w = int(floor(f * arctan((w - w/2)/f) + f * arctan(w / (2*f))))
    new_h = h
    new_img = Image.new(img.mode, (new_w, new_h))

    for y in range(new_h):
        for x in range(new_w):
            new_x = floor(f * tan(x / f - arctan(w / (2*f))) + w/2)
            new_y = floor((y-h/2)*sqrt((new_x - w/2)**2 + f**2)/f + h/2)

            if new_x >= 0 and new_x < w and new_y >= 0 and new_y < h:
                new_img.putpixel((x,y), img.getpixel((new_x, new_y)))

    return new_img

def merge(img1, kp1, img2, kp2, matches):
    w1, h1 = img1.size
    w2, h2 = img2.size

    distance_x, distance_y = 0, 0

    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # col: x, row: y
        x1, y1 = kp1[img1_idx].pt
        x2, y2 = kp2[img2_idx].pt

        distance_x += (x2 - x1)
        distance_y += (y2 - y1)

    # offset of img2
    distance_x = int(floor(distance_x / len(matches)))
    distance_y = int(floor(distance_y) / len(matches))

    # judge the how the direciton should set, set flag
    if distance_x <= 0:
        distance_x += w1
        flag = True # img1 on the left
    else:
        distance_x = w1 - distance_x
        distance_y = 0 - distance_y
        flag = False

    new_w = w1 + w2 - distance_x
    new_h = h1 + distance_y if flag else h2 + distance_y

    out = Image.new(img1.mode, (new_w, new_h))

    for y in range(new_h):
        for x in range(new_w):
            if (x <= w1 - distance_x):
                if flag:
                    out.putpixel((x, y), img1.getpixel((x, y)))
                else:
                    out.putpixel((x, y), img2.getpixel((x, y)))
            else:
                offset_y = y + distance_y if y + distance_y >= 0 and y + distance_y < h1 else y
                if flag:
                  out.putpixel((x, y), img2.getpixel((x - (w1 - distance_x), offset_y)))
                else:
                  out.putpixel((x, y), img1.getpixel((x - (w1 - distance_x), offset_y)))

    return out


def main():
    print "Cylindrical projection now."
    pic = cylindrical_projection(Image.open(sys.argv[1])) # query
    pic2 = cylindrical_projection(Image.open(sys.argv[2])) #train
    print "Cylindrical projection finished."

    print "Find Speeded-Up Robust Features."
    sift = cv2.SIFT(500)
    sift2 = cv2.SIFT(500)
    keypoint, descriptor = sift.detectAndCompute(array(pic), None)
    keypoint2, descriptor2 = sift2.detectAndCompute(array(pic2), None)
    print "Finish Speeded-Up Robust Features."

    print "Match descriptors."
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptor, descriptor2, k=2)

    good = []
    alpha = 0.1
    while (len(good) == 0):
        good = []
        for m, n in matches:
            if m.distance < alpha * n.distance:
                good.append(m)
        alpha += 0.2
    print "Finish matching."

    print "According matches to create a new image."
    result = merge(pic, keypoint, pic2, keypoint2, good)
    print "Finish creating."

    print "Save to ./result.jpg."
    result.save('result.jpg')
    print "Finish saving."

if __name__ == '__main__':
    main()