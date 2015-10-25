#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from PIL import Image
from PyQt4 import QtGui

# Create an empty window
class main_window(QtGui.QMainWindow):
  def __init__(self):
    super(main_window, self).__init__()

    self.current = None # file to open

    self.initUI()
    self.show()
  
  def initUI(self):
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

    # Menu Bar
    menu = self.menuBar()
    menu.setMinimumHeight(25)
    file_menu = menu.addMenu('&File')
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(exit_action)

    # Status Bar
    self.statusBar()

    # Image Holder
    self.container = QtGui.QLabel(self)
    self.container.move(20, 35)

    # Basic UI
    self.moveMain(500, 500)
    self.setWindowTitle('Digital Image Process Tool')

  def moveMain(self, w, h):
    if w <= 500 or h <= 500:
      return
    screen = QtGui.QDesktopWidget().screenGeometry()
    self.resize(w, h)
    self.move((screen.width() - w) / 2, (screen.height() - h) / 2)

  def show_open_dialog(self):
    filename = QtGui.QFileDialog.getOpenFileName(self, 'Please choose a picture', \
        os.path.expanduser('~'), 'Images (*.bmp *.jpg *.png)')

    self.current = Image.open(unicode(filename.toUtf8(), 'utf-8', 'ignore')) # mysterious transform...

    width, height = self.current.size
    pixmap = QtGui.QPixmap(filename)
    self.container.setPixmap(pixmap)

    # Adjust position
    self.container.setFixedSize(width, height)
    self.moveMain(width + 40, height + 55) # 20 padding left-right, 10 padding up-down
    self.setWindowTitle('Digital Image Process Tool (' + filename + ')')
    self.show()

  def show_save_dialog(self):
    filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Image To', \
        os.path.expanduser('~'), 'bmp file (*.bmp);;jpeg file (*.jpg);;png file (*.png)', \
        None, QtGui.QFileDialog.ShowDirsOnly)

    self.current.save(unicode(filename.toUtf8(), 'utf-8', 'ignore'))

# Main
def main():
  app = QtGui.QApplication(sys.argv)
  w = main_window()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
