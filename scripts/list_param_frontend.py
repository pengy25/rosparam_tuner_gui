#! /usr/bin/env python
import Tkinter as tk
import rospy

class ParamList(tk.Frame):
  def __init__(self, container):
    tk.Frame.__init__(self, container)
    self.paramList = tk.Listbox(self)

    params = rospy.get_param_names()

    for param in params:
      self.paramList.insert(tk.END, param)

    self.paramList.pack(fill=tk.BOTH, expand=tk.YES)
  

def main():
  rospy.init_node("list_param_node")
  while rospy.Time.now().to_sec() == 0:
    pass

  window = tk.Tk()

  majorFrame = ParamList(window)
  majorFrame.pack(fill=tk.BOTH, expand=tk.YES)

  tk.mainloop()

if __name__ == "__main__":
  main()
