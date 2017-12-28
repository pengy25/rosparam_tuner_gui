#! /usr/bin/env python
import Tkinter as tk
import rospy
from .single_param_frame import SingleParamFrame

# This frame provides the functionality to adjust the number of ROS parameters to work on
class MultiParamFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    tk.Frame.grid_columnconfigure(self, 1, weight=1)
    self.addButton = tk.Button(self, text="+", command=self.addParamFrame)
    self.addButton.grid(row=0, columnspan=2, sticky=tk.W + tk.E)
    self.itemLst = []
    self.counter = 0

  def emptyFrame(self):
    self.addButton.grid_forget()

    for serial_num, deleteButton, item in self.itemLst:
      deleteButton.grid_forget()
      item.grid_forget()

  def fillFrame(self):
    for i in range(len(self.itemLst)):
      self.itemLst[i][1].grid(row=i, column=0)
      self.itemLst[i][2].grid(row=i, column=1, sticky=tk.W+tk.E)
    
    self.addButton.grid(row=len(self.itemLst), columnspan=2,  sticky=tk.W + tk.E)

  def getParams(self):
    res = {}
    for serial_num, deleteButton, item in self.itemLst:
      param_name, val_type, param_val = item.getParam()
      if val_type == "int":
        param_val = int(param_val)
      elif val_type == "float":
        param_val = float(param_val)

      res[param_name] = param_val

    return res

  def addParamFrame(self, param_name="param_name", param_val="param_val", val_type="string"):
    self.emptyFrame()

    item = SingleParamFrame(self, param_name=param_name, param_val=param_val, val_type=val_type)
    deleteButton = tk.Button(self, text="-", command=lambda num=self.counter: self.deleteParamFrame(num))
    self.itemLst.append((self.counter, deleteButton, item))
    self.counter += 1

    self.fillFrame()

  def addParamFrames(self, params):
    for param_name, param_val in params.iteritems():
      val_type = "string"
      if type(param_val) is int:
        val_type = "int"
      elif type(param_val) is float:
        val_type = "float"

      self.addParamFrame(param_name, param_val, val_type)

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

