#! /usr/bin/env python
import Tkinter as tk
import rospy

# This frame provides a list of the existing ROS parameters in the environment.
# However, this frame doesn't updates itself automatically when the parameters
# in the environment are modified. In addition, users can use right mouse key to
# obtain the option to call the callback on a list element name.
class ParamListFrame(tk.Frame):
  def __init__(self, container, callback=None):
    tk.Frame.__init__(self, container)
    self.scrollbar = tk.Scrollbar(self)
    self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
    self.scrollbar.config(command=self.listbox.yview)

    params = rospy.get_param_names()

    for param in params:
      self.listbox.insert(tk.END, param)

    # Binds the right click event to the popup menu
    self.menu = PopupMenu(self.listbox)
    self.listbox.bind("<Button-3>", self.menu.popup_callback)
    self.menu.add_command(label="Add this param to edit",\
     command=self.add_param_callback)

    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.callback = callback

  # The callback to handle what to do when the menu option is chosen, as
  # listbox elements are selected.
  def add_param_callback(self):
      selectedParam = [self.listbox.get(i) for i in self.listbox.curselection()]
      for param in selectedParam:
          if (self.callback is not None):
            self.callback(param)
          else:
            print "Selected", param

  def update(self):
    self.listbox.delete(0, tk.END)

    params = rospy.get_param_names()

    for param in params:
      self.listbox.insert(tk.END, param)

# This is a helper class for a popup menu
class PopupMenu(tk.Menu):
  def __init__(self, container):
    tk.Menu.__init__(self, container, tearoff=0)

  # The callback to handle popup menu
  def popup_callback(self, e):
    try:
      self.tk_popup(e.x_root, e.y_root, 0)
    finally:
      self.grab_release()
