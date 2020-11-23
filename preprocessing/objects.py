import json

def pretty(d, indent=0):
  result = ''
  for key, value in d.items():
    result += '\t' * indent + str(key) + ': '
    if isinstance(value, dict):
      result += pretty(value, indent+1) + '\n'
    else:
      result += str(value) + '\n'
  return result

def pretty_json(d, offset=''):
  res = offset + '{\n'
  for key, value in d.items():
    res += offset + '\t"' + str(key) + '": '
    if isinstance(value, dict):
      res += '\n' + pretty_json(value, offset + '\t') + ',\n'
    else:
      if str(value) == '§':
        value = '"§"'
      else:
        value = str(value)
      res += str(value) + ',\n'
  if len(d) == 0:
    return res[:-1] + '\n' + offset + '}'
  else:
    return res[:-2] + '\n' + offset + '}'

import copy

class Alert:
  def __init__(self, dictionary):
    self.d = dictionary
    self.file = None # For evaluation
    self.pretty_print = True
    self.noise = False # For evaluation; true if alert is manually added as noise

  def get_json_representation(self, offset=''):
    return pretty_json(self.d, offset)

  def get_alert_clone(self):
    clone = Alert(copy.deepcopy(self.d))
    clone.file = self.file
    clone.pretty_print = self.pretty_print
    clone.noise = self.noise
    return clone

  def __repr__(self):
    if self.pretty_print:
      return pretty(self.d)
    else:
      return str(self.d)
