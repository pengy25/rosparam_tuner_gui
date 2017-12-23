#! /usr/bin/evn python
import rospy
import yaml

# This function reads the given yaml file and load the supported value types only
def readDumpFile(filename):
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
