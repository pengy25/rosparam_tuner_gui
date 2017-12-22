#! /usr/bin/env python
import Tkinter as tk
import rospy

# This frame provides a list of the existing ROS parameters in the environment.
# However, this frame doesn't updates itself automatically when the parameters
# in the environment are modified.
class ParamListFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    self.scrollbar = tk.Scrollbar(container)
    self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
    self.scrollbar.config(command=self.listbox.yview)

    params = rospy.get_param_names()

    for param in params:
      self.listbox.insert(tk.END, param)

    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

  def update(self):
    self.listbox.delete(0, tk.END)

    params = rospy.get_param_names()

    for param in params:
      self.listbox.insert(tk.END, param)

