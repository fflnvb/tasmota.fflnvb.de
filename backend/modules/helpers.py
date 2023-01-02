#!/usr/bin/python

import json

# Solution by Eric Leschinski & Kirill Zaitsev: https://stackoverflow.com/questions/5508509/how-do-i-check-if-a-string-is-valid-json-in-python
def isJson(inputString):
  try:
    json.loads(inputString)
  except ValueError as e:
    return False
  return True