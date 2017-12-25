#! /usr/bin/evn python
import rospy
import yaml
from tkFileDialog import askopenfilename, asksaveasfilename

# This function gives a dialog to obtain the yaml file and load the supported value types only
def readDumpFileDialog(window):
  filename = askopenfilename(parent=window, title="Gives a file name", defaultextension=".yaml", filetypes=[("YAML file", "*.yaml")])

  if filename:
    fd = open(filename, "r")
    content = yaml.safe_load(fd.read())
    fd.close()
  
    # Filter out the unsupported value type
    res = {}  
    for key, value in content.iteritems():
      if (type(value) is not int and type(value) is not str and type(value) is not float):
        continue
  
      # Remove newlines
      tmp_val = value
      if type(tmp_val) is str:
        tmp_val = tmp_val.strip()
  
      res[key.strip()] = tmp_val
  
    return res

# This function dump the given dictionary into a yaml file with the file name specified through a dialog
def writeDumpFileDialog(window, content):
  filename = asksaveasfilename(parent=window, title="Gives a file name", defaultextension=".yaml", filetypes=[("YAML file", "*.yaml")])

  if filename:
    fd = open(filename, "w+")

    yaml.dump(content, fd, default_flow_style=False)
    fd.close()
