#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from bisect import bisect_right

from PIL import Image
from PyQt4 import QtGui

# Create an empty window
class main_window(QtGui.QMainWindow):
  def __init__(self):
    super(main_window, self).__init__()

    self.current = None # file to open

    self.initUI()
    self.show()

    # self constants
    self.TEMP = 'gui.dipthumb'
  
  def initUI(self):
    ''' UI initialize
    UI and events binding
    '''
    # exit action
    exit_action = QtGui.QAction('Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit application')
    exit_action.triggered.connect(self.close)

    # open file dialog
    open_action = QtGui.QAction('Open', self)
    open_action.setShortcut('Ctrl+O')
    open_action.setStatusTip('Open file')
    open_action.triggered.connect(self.show_open_dialog)

    # save file to
    save_action = QtGui.QAction('Save As', self)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save file')
    save_action.triggered.connect(self.show_save_dialog)

    # binarization
    binarization = QtGui.QAction('Binarization', self)
    binarization.setStatusTip('Binarize the image')
    binarization.triggered.connect(self.binarize)

    # quantization
    quantization = QtGui.QAction('Quantization', self)
    quantization.setStatusTip('Quantize the image')
    quantization.triggered.connect(self.quantize)

    # Menu Bar
    menu = self.menuBar()
    menu.setMinimumHeight(25)
    file_menu = menu.addMenu('&File')
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(exit_action)
    process_menu = menu.addMenu('&Transform')
    process_menu.addAction(binarization)
    process_menu.addAction(quantization)

    # Status Bar
    self.statusBar()

    # Image Holder
    self.container = QtGui.QLabel(self)
    self.container.move(20, 35)

    # Basic UI
    self.move_main(500, 500)
    self.setWindowTitle('Digital Image Process Tool')

  def move_main(self, w, h):
    ''' Helper
    Move the window to the screen center
    '''
    if w < 500 or h < 500:
      return
    screen = QtGui.QDesktopWidget().screenGeometry()
    self.resize(w, h)
    self.move((screen.width() - w) / 2, (screen.height() - h) / 2)

  def update_image(self):
    ''' Update image
    Update image after processing
    '''
    w, h = self.current.size
    self.current.save(self.TEMP, self.current.format)
    pixmap = QtGui.QPixmap(self.TEMP)
    self.container.setPixmap(pixmap)

    self.container.setFixedSize(w, h)
    self.move_main(w + 40, h + 55) # 20 padding left-right, 10 padding up-down
    self.show()

  def show_open_dialog(self):
    ''' Open File
    You can only choose image files
    '''
    filename = QtGui.QFileDialog.getOpenFileName(self, 'Please choose a picture', \
        os.path.expanduser('~'), 'Images (*.bmp *.jpg *.png)')

    self.current = Image.open(unicode(filename.toUtf8(), 'utf-8', 'ignore')) # mysterious transform...

    self.update_image()

  def show_save_dialog(self):
    ''' Save File
    Save current image to~
    '''
    filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Image To', \
        os.path.expanduser('~'), 'bmp file (*.bmp);;jpeg file (*.jpg);;png file (*.png)', \
        None, QtGui.QFileDialog.ShowDirsOnly)

    self.current.save(unicode(filename.toUtf8(), 'utf-8', 'ignore'))

  def binarize(self):
    ''' Binarization
    Binarize the image~
    '''
    self.quantize(2)

  def quantize(self, level = None):
    ''' Binarization
    Binarize the image with level
    '''
    if not self.current:
      ok = QtGui.QMessageBox.critical(self, 'Wrong behavior', 'You have not opened a file yet!')
      if (ok == QtGui.QMessageBox.Ok):
        return
    
    if not (self.current.mode in ['L', 'RGB']):
      ok = QtGui.QMessageBox.critical(self, 'Wrong image', 'I can only process RGB / grayscale image!')
      if (ok == QtGui.QMessageBox.Ok):
        return

    if not level:
      level, ok = QtGui.QInputDialog.getInt(self, 'Please input the level you want to quantize to:',\
        'Level:', 0, 1, 255, 1)
 
    # judge level first, so level 2 pass~
    if level or ok:
      palette = [255 * p / (level - 1) for p in range(level)]
      w, h = self.current.size

      for y in range(h):
        for x in range(w):
          p = self.current.getpixel((x,y))
          if self.current.mode == 'RGB':
            p = p[0]

          i = bisect_right(palette, p)
          if i == len(palette) or palette[i] - p > p - palette[i-1]:
            out_p = palette[i-1]
          else:
            out_p = palette[i]

          if self.current.mode == 'RGB':
            out_p = (out_p, out_p, out_p)

          self.current.putpixel((x,y), out_p)

      self.update_image()

  def closeEvent(self, e):
    if self.TEMP in os.listdir(os.getcwd()):
      os.remove(self.TEMP)
    super(main_window, self).closeEvent(e)

# Main Function
def main():
  app = QtGui.QApplication(sys.argv)
  w = main_window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
