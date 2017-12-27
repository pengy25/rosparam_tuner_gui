#! /usr/bin/env python
import Tkinter as tk
from .utility import readDumpFileDialog, writeDumpFileDialog

# This menu is expected to be contained by the main window, and it
# provides a menu near the top of the window for file input/ouput.
class WindowMenu(tk.Menu):
  def __init__(self, window, get_data_command, write_data_command):
    tk.Menu.__init__(self, window)
    window.config(menu=self)

    self.iomenu = tk.Menu(self)
    self.iomenu.add_command(label="Read params from a file", command=self.readDataHelper)
    self.iomenu.add_command(label="Write params to a file", command=self.writeDataHelper)

    tk.Menu.add_cascade(self, label="File", menu=self.iomenu)

    self.window = window
    self.get_data_command = get_data_command
    self.write_data_command = write_data_command

  def writeDataHelper(self):
    content = self.get_data_command()
    writeDumpFileDialog(self.window, content)

  def readDataHelper(self):
    content = readDumpFileDialog(self.window)
 
    for param_name, param_val in content.iteritems():
      self.write_data_command(param_name, param_val)
