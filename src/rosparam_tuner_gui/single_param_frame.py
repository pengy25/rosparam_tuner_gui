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
    if self._val_type.get() == "string":
      pass
    elif self._val_type.get() == "int":
      val = int(val)
    elif self._val_type.get() == "float":
      val = float(val)
    else:
      self._param_val.set("value type not supported")
      return

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
  def __init__(self, container, param_name="param name", param_val="param value", *args):
    tk.Frame.__init__(self, container, args)
    tk.Label(self, text="rosparam").pack(side=tk.LEFT)

    param_name = tk.StringVar()
    param_val = tk.StringVar()
    val_type = tk.StringVar()
    param_name.set("param name")
    param_val.set("param value")
    val_type.set("value type")

    DeleteButton(self, "Delete", param_name, param_val).pack(side=tk.LEFT)
    GetButton(self, "Get", param_name, param_val).pack(side=tk.LEFT)
    SetButton(self, "Set", param_name, val_type, param_val).pack(side=tk.LEFT)

    tk.Entry(self, textvariable=param_name).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.OptionMenu(self, val_type, "string", "int", "float").pack(side=tk.LEFT)
    tk.Entry(self, textvariable=param_val).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

