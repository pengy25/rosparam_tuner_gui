#! /usr/bin/env python
import Tkinter as tk
import rospy
from single_param_frontend import ParamFrame

class ListFrame(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    tk.Frame.grid_columnconfigure(self, 1, weight=1)
    self.addButton = tk.Button(self, text="+", command=self.add_callback)
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

  def add_callback(self):
    self.emptyFrame()

    item = ParamFrame(self)
    deleteButton = tk.Button(self, text="-", command=lambda num=self.counter: self.delete_callback(num))
    self.itemLst.append((self.counter, deleteButton, item))
    self.counter += 1

    self.fillFrame()

  def delete_callback(self, num):
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

def main():
  rospy.init_node("multiparam_node")
  while rospy.Time.now().to_sec() == 0:
    pass

  window = tk.Tk()
  majorFrame = ListFrame(window)
  majorFrame.pack(fill=tk.BOTH, expand=tk.YES)

  window.mainloop()

if __name__ == "__main__":
  main()
