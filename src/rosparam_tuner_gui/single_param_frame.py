#! /usr/bin/env python
import Tkinter as tk
import rospy

# Generic class for buttons connected with parameter name and value
class ParamButton(tk.Button):
  def __init__(self, container, text, param_name, param_val):
    self._param_name = param_name
    self._param_val = param_val
    tk.Button.__init__(self, container, text=text, command=self.callback)

  def callback(self):
    print "param name:", self._param_name.get()
    print "param val:", self._param_val.get()

# Button that supports 'rosparam get'
class GetButton(ParamButton):
  def __init__(self, *args):
    ParamButton.__init__(self, *args)

  def callback(self):
    if rospy.has_param(self._param_name.get()):
      self._param_val.set(rospy.get_param(self._param_name.get()))
    else:
      self._param_val.set("param name not found") 

# Button that supports 'rosparam set'
class SetButton(ParamButton):
  def __init__(self, container, text, param_name, val_type, param_val):
    self._val_type = val_type
    ParamButton.__init__(self, container, text, param_name, param_val)

  def callback(self):
    val = self._param_val.get()
    if self._val_type.get() == "int":
      val = int(val)
    elif self._val_type.get() == "float":
      val = float(val)
    
    rospy.set_param(self._param_name.get(), val)

# Button that supports 'rosparam delete'
class DeleteButton(ParamButton):
  def __init__(self, *args):
    ParamButton.__init__(self, *args)

  def callback(self):
    try:
      rospy.delete_param(self._param_name.get())
    except KeyError:
      self._param_val.set("param name not found")

# A single frame that provides interaction with a specified ROS parameter
class SingleParamFrame(tk.Frame):
  def __init__(self, container, param_name="param_name", param_val="param_value", val_type="string", *args):
    tk.Frame.__init__(self, container, args)
    tk.Label(self, text="rosparam").pack(side=tk.LEFT)

    self.param_name = tk.StringVar()
    self.param_val = tk.StringVar()
    self.val_type = tk.StringVar()
    self.param_name.set(param_name)
    self.param_val.set(param_val)
    self.val_type.set(val_type)  # Assume default type is string

    DeleteButton(self, "Delete", self.param_name, self.param_val).pack(side=tk.LEFT)
    GetButton(self, "Get", self.param_name, self.param_val).pack(side=tk.LEFT)
    SetButton(self, "Set", self.param_name, self.val_type, self.param_val).pack(side=tk.LEFT)

    tk.Entry(self, textvariable=self.param_name).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.OptionMenu(self, self.val_type, "string", "int", "float").pack(side=tk.LEFT)
    tk.Entry(self, textvariable=self.param_val).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

  def getParam(self):
    return (self.param_name.get(), self.val_type.get(), self.param_val.get())

  def setParam(self):
    val = self.param_val.get()
    if self.val_type == "int":
      val = int(val)
    elif self.val_type == "float":
      val = float(val)

    rospy.set_param(self.param_name.get(), val)
