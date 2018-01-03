#! /usr/bin/env python
import Tkinter as tk
import rospy
import yaml

# Generic class for buttons connected with parameter name and value
class ParamButton(tk.Button):
  def __init__(self, container, text, param_name, param_val, val_type):
    self._param_name = param_name
    self._param_val = param_val
    self._val_type = val_type
    tk.Button.__init__(self, container, text=text, command=self.callback)

  def callback(self):
    print "param name:", self._param_name.get()
    print "param val:", self._param_val.get()
    print "val type:", self._val_type.get()

# Button that supports 'rosparam get'
class GetButton(ParamButton):
  def __init__(self, *args):
    ParamButton.__init__(self, *args)

  def callback(self):
    if rospy.has_param(self._param_name.get()):
      target = rospy.get_param(self._param_name.get())
      self._val_type.set(type(target))

      if type(target) is bool:
        if target:
          target = "true"
        else:
          target = "false"

      self._param_val.set(target)

    else:
      self._param_val.set("param name not found")
      self._val_type.set("some undetermined value type") 

# Button that supports 'rosparam set'
class SetButton(ParamButton):
  def __init__(self, container, *args):
    ParamButton.__init__(self, container, *args)

  def callback(self):
    yaml_str = self._param_name.get() + ": " + self._param_val.get()
    res = yaml.safe_load(yaml_str)

    if len(res) != 1:
      print "Warning: a SetButton doesn't support multiple param setup"
      return

    for param_name, param_val in res.iteritems():
      self._val_type.set(type(param_val))
      rospy.set_param(param_name, param_val)

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
  def __init__(self, container, param_name="param_name", param_val="param_value", *args):
    tk.Frame.__init__(self, container, args)
    tk.Label(self, text="rosparam").pack(side=tk.LEFT)

    self.param_name = tk.StringVar()
    self.param_val = tk.StringVar()
    self.val_type = tk.StringVar()
    self.param_name.set(param_name)
    self.param_val.set(param_val)
    self.val_type.set("some undetermined value type")

    DeleteButton(self, "Delete", self.param_name, self.param_val, self.val_type).pack(side=tk.LEFT)
    GetButton(self, "Get", self.param_name, self.param_val, self.val_type).pack(side=tk.LEFT)
    self.setButton = SetButton(self, "Set", self.param_name, self.param_val, self.val_type)
    self.setButton.pack(side=tk.LEFT)

    tk.Entry(self, textvariable=self.param_name).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.Entry(self, textvariable=self.param_val).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    tk.Label(self, text=" of ").pack(side=tk.LEFT)
    tk.Label(self, textvariable=self.val_type).pack(side=tk.LEFT)

  def getParam(self):
    yaml_str = self.param_name.get() + ": " + self.param_val.get()
    res = yaml.safe_load(yaml_str)

    if (len(res) != 1):
      print "Warning: SingleParam detects multiple param_name"
      return None

    for param_name, param_val in res.iteritems():
      return (param_name, param_val)

  def setParam(self):
    self.setButton.callback()
