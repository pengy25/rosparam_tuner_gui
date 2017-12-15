#! /usr/bin/env python
import Tkinter as tk
import rospy
from single_param_frontend import ParamFrame

class ItemFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    self.deleteButton = tk.Button(self, text="-", command=self.callback)
    self.paramFrame = ParamFrame(self)
    self.deleteButton.pack(side=tk.LEFT)
    self.paramFrame.pack(side=tk.LEFT)

  def callback(self):
    self.deleteButton.pack_forget()
    self.paramFrame.pack_forget()

    self.deleteButton.destroy()
    self.paramFrame.destroy()

    tk.Frame.pack_forget(self)
    tk.Frame.destroy(self)

class ListFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    self.addButton = tk.Button(self, text="+", width=80, command=self.callback)
    self.addButton.pack(fill=tk.X)

  def callback(self):
    self.addButton.pack_forget()
    ItemFrame(self).pack(fill=tk.X)
    self.addButton.pack(fill=tk.X)

def main():
  rospy.init_node("multiparam_node")
  while rospy.Time.now().to_sec() == 0:
    pass

  window = tk.Tk()
  majorFrame = ListFrame(window)
  majorFrame.pack(fill=tk.X)

  window.mainloop()

if __name__ == "__main__":
  main()
