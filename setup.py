from PyQt5 import QtWidgets

from src.mainwindow import MainWindow

import sys

def create_and_run_app():
  app = create_app()
  window = create_main_window()
  window.display()
  run_app_until_exit(app)

def create_app():
  return QtWidgets.QApplication(sys.argv)

def create_main_window():
  return MainWindow()

def run_app_until_exit(app):
  sys.exit(app.exec_())

if __name__ == '__main__':
  create_and_run_app()
