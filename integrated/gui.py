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
    binarization.setStatusTip('Binarize the picture, only make sense to grayscale image.')
    binarization.triggered.connect(self.binarize)

    # Menu Bar
    menu = self.menuBar()
    menu.setMinimumHeight(25)
    file_menu = menu.addMenu('&File')
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(exit_action)
    process_menu = menu.addMenu('&Transform')
    process_menu.addAction(binarization)

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
    if (self.current.mode != 'L'):
      return

    w, h = self.current.size
    for y in range(h):
      for x in range(w):
        p = self.current.getpixel((x, y))
        if p <= 127:
          self.current.putpixel((x, y), 0)
        else:
          self.current.putpixel((x, y), 255)

    self.update_image()

# Main Function
def main():
  app = QtGui.QApplication(sys.argv)
  w = main_window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
