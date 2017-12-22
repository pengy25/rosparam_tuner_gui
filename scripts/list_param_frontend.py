#! /usr/bin/env python
import Tkinter as tk
import rospy

class ParamList(tk.Frame):
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

def main():
  rospy.init_node("list_param_node")
  while rospy.Time.now().to_sec() == 0:
    pass

  window = tk.Tk()

  frame1 = tk.Frame(window)
  frame1.pack(fill=tk.BOTH, expand=tk.YES)

  paramList = ParamList(frame1)
  paramList.pack(fill=tk.BOTH, expand=tk.YES)

  frame2 = tk.Frame(window)
  frame2.pack(fill=tk.X, expand=tk.YES)

  tk.Button(frame2, text="Update", command=paramList.update).pack(side=tk.RIGHT)

  tk.mainloop()

if __name__ == "__main__":
  main()
