from PIL import Image

import os

# nearest neighbor inter
def scaleNNI(input_img, size):
  in_size = input_img.size
  in_width, in_height = in_size
  out_width, out_height = size

  width_ratio = in_width / out_width
  height_ratio = in_height / out_height

  out_pixels = []

  for out_y in range(out_height):
    row = []
    for out_x in range(out_width):
      in_x = round(float(out_x) * width_ratio)
      in_y = round(float(out_y) * height_ratio)
      row.append(input_img.getpixel((in_x, in_y)))
    out_pixels.append(row)
  
  return createImage(input_img.mode, size, out_pixels)

def createImage(mode, size, pixels):
  out = Image.new(mode, size)

  for y in range(size[1]):
    for x in range(size[0]):
      out.putpixel((x,y), pixels[y][x])

  return out
  
def testScale(filename):
  im = Image.open(filename)
  result = scaleNNI(im, (192,128))
  result_name = 'scale-192-128.png'
  result.save("../dist/" + result_name)

def main():
  testScale("../assets/43.png")

if __name__ == "__main__":
  main()
