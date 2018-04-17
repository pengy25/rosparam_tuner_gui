#! /usr/bin/env python
import Tkinter as tk
import rospy
from .single_param_frame import SingleParamFrame

# This class is a frame of three buttons: 'Delete all params', 'Set all params',
# 'Get all params'
class ThreeButtonFrame(tk.Frame):
  def __init__(self, container, delete_command, set_command, get_command):
    tk.Frame.__init__(self, container)
    tk.Button(self, text="Delete all params",\
    command=delete_command).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.Button(self, text="Set all params",\
    command=set_command).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.Button(self, text="Get all params",\
    command=get_command).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

# This frame provides the functionality to adjust the number of ROS parameters
# to work on
class MultiParamFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    tk.Frame.grid_columnconfigure(self, 1, weight=1)
    self.addButton = tk.Button(self, text="+", command=self.addParamFrame)
    self.addButton.grid(row=1, columnspan=2, sticky=tk.W + tk.E)
    self.itemLst = []
    self.counter = 0
    self.buttonFrame = ThreeButtonFrame(self, self.delete_all, self.set_all,\
    self.get_all)
    self.buttonFrame.grid(row=0, column=1, sticky=tk.W + tk.E)

  def delete_all(self):
    for serial_num, deleteButton, item in self.itemLst:
      item.deleteParam()

  def set_all(self):
    for serial_num, deleteButton, item in self.itemLst:
      item.setParam()

  def get_all(self):
    for serial_num, deleteButton, item in self.itemLst:
      item.getParam()

  def emptyFrame(self):
    self.addButton.grid_forget()

    for serial_num, deleteButton, item in self.itemLst:
      deleteButton.grid_forget()
      item.grid_forget()

  def fillFrame(self):
    for i in range(len(self.itemLst)):
      self.itemLst[i][1].grid(row=i+1, column=0)
      self.itemLst[i][2].grid(row=i+1, column=1, sticky=tk.W+tk.E)

    self.addButton.grid(row=len(self.itemLst)+1, columnspan=2,\
    sticky=tk.W + tk.E)

  def exportParams(self):
    res = {}
    for serial_num, deleteButton, item in self.itemLst:
      param_name, param_val = item.exportParam()

      res[param_name] = param_val

    return res

  def addParamFrame(self, param_name="param_name", param_val="param_val"):
    self.emptyFrame()

    item = SingleParamFrame(self, param_name=param_name, param_val=param_val)
    deleteButton = tk.Button(self, text="-",\
    command=lambda num=self.counter: self.deleteParamFrame(num))
    self.itemLst.append((self.counter, deleteButton, item))
    self.counter += 1

    self.fillFrame()

  def addParamFrames(self, params):
    for param_name, param_val in params.iteritems():

      self.addParamFrame(param_name, param_val)

  def deleteParamFrame(self, num):
    self.emptyFrame()

    tmp = self.itemLst
    self.itemLst = []

    for serial_num, deleteButton, item in tmp:
      if (serial_num != num):
        self.itemLst.append((serial_num, deleteButton, item))
      else:
        deleteButton.destroy()
        item.destroy()

    self.fillFrame()
