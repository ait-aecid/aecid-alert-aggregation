from merging.merge import merge_json
import json
from merging.objects import Wildcard
from merging.objects import Mergelist

def createOutput(jsons, lim, min_key_freq, min_val_freq):
  i = 1
  for j in jsons:
    print('Json' + str(i) + ' = ' + str(j))
    i += 1
  print('Merge = ' + str(merge_json(jsons, lim, min_key_freq, min_val_freq)))
  print('')

base = """
{
  "A": "a",
  "B": 1,
  "C": [
    "c", 
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

j0 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Identical')
createOutput([json.loads(base), json.loads(j0)], 3, 0.0, 0.0)

j1 =  """
{
  "A": "x",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Value A different')
createOutput([json.loads(base), json.loads(j1)], 3, 0.0, 0.0)

j2 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    2
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('List C different')
createOutput([json.loads(base), json.loads(j2)], 3, 0.0, 0.0)

j3 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": false,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Subvalue D1 different')
createOutput([json.loads(base), json.loads(j3)], 3, 0.0, 0.0)

j4 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "dx.y",
      "d2.3"
    ]
  }
}"""

print('Sublist D2 different')
createOutput([json.loads(base), json.loads(j4)], 3, 0.0, 0.0)

j5 =  """
{
  "A": "b",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

j6 =  """
{
  "A": "c",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Value A three times different')
createOutput([json.loads(base), json.loads(j5), json.loads(j6)], 3, 0.0, 0.0)

j7 =  """
{
  "A": "d",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Value A four times different')
createOutput([json.loads(base), json.loads(j5), json.loads(j6), json.loads(j7)], 3, 0.0, 0.0)

j8 =  """
{
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Value A min key occurrence 0.7')
createOutput([json.loads(base), json.loads(j5), json.loads(j6), json.loads(j7), json.loads(j8)], 3, 0.7, 0.0)

print('Value A min key occurrence 0.9')
createOutput([json.loads(base), json.loads(j5), json.loads(j6), json.loads(j7), json.loads(j8)], 3, 0.9, 0.0)

print('Value A min val occurrence 0.7')
createOutput([json.loads(base), json.loads(base), json.loads(base), json.loads(base), json.loads(j7)], 3, 0.0, 0.7)

print('Value A min val occurrence 0.9')
createOutput([json.loads(base), json.loads(base), json.loads(base), json.loads(base), json.loads(j7)], 3, 0.0, 0.9)

j9 = """
{
  "A": "a1",
  "B": "b1",
  "C": "c1",
  "D": "d1"
}
"""

j10 = """
{
  "A": "a1",
  "B": "b2",
  "C": "c2"
}
"""

j11 = """
{
  "A": "a1",
  "B": "b1",
  "C": "c3"
}
"""

print('Sample for presentation')
createOutput([json.loads(j9), json.loads(j10), json.loads(j11)], 2, 0.5, 0.0)
