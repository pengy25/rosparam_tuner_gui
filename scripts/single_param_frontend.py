#! /usr/bin/env python
import Tkinter as tk
import rospy

window = tk.Tk()

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

# Test code for GUI
def main():
  rospy.init_node("single_param_node")
  while rospy.Time.now().to_sec() == 0:
    pass

  majorFrame = tk.Frame(window)
  majorFrame.pack()

  tk.Label(majorFrame, text="rosparam").grid(row=0, column=0)

  param_name = tk.StringVar()
  param_val = tk.StringVar()
  val_type = tk.StringVar()
  param_name.set("param name")
  param_val.set("param value")
  val_type.set("value type")

  GetButton(majorFrame, "Get", param_name, param_val).grid(row=0, column=1)
  SetButton(majorFrame, "Set", param_name, val_type, param_val).grid(row=0, column=2)

  tk.Entry(majorFrame, textvariable=param_name).grid(row=0, column=3)
  tk.OptionMenu(majorFrame, val_type, "string", "int", "float").grid(row=0, column=4)
  tk.Entry(majorFrame, textvariable=param_val).grid(row=0, column=5)

  window.mainloop()

if __name__ == '__main__':
  main()
