from merging.merge import merge_group, merge_bag
import json
from merging.objects import Wildcard
from merging.objects import Mergelist
from preprocessing.objects import Alert
from clustering.objects import Group

def createOutput(groups, min_alert_match_similarity=0.0):
  i = 0
  for group in groups:
    print('Group ' + str(i))
    i += 1
    for alert in group.alerts:
      print(alert.d)
  merge = merge_group(groups, min_alert_match_similarity=min_alert_match_similarity)
  print('Merge = ')
  for alert in merge.alerts:
    print(alert.d)
  print('')

def createOutput_bag(groups):
  i = 0
  for group in groups:
    group.create_bag_of_alerts(0.8, None, 0.0, 0.0)
    print('Group ' + str(i))
    i += 1
    print(group)
    #for alert_pattern, freq in group.bag_of_alerts.items():
    #  print(str(freq)alert_pattern)
  merge = merge_group(groups, 0.5)
  print('Merge = ')
  print(merge)
  print('')

def createOutput_alignment(groups):
  i = 0
  for group in groups:
    group.create_bag_of_alerts(0.8, None, 0.0, 0.0)
    print('Group ' + str(i))
    i += 1
    print(group)
    #for alert_pattern, freq in group.bag_of_alerts.items():
    #  print(str(freq)alert_pattern)
  merge = merge_group(groups, 0.5)
  print('Merge = ')
  for alert in merge.merge_seq:
    print(alert)
  print('')

base_1 = """
{
  "A": "a1",
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

base_2 =  """
{
  "A": "a2",
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

base_3 =  """
{
  "A": "a3",
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

j_1 = """
{
  "A": "a1",
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

j_2 =  """
{
  "A": "a2",
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

j_3 =  """
{
  "A": "a3",
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
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3))])
createOutput([g1, g2])

print('Change order of two alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_2)), Alert(json.loads(j_1)), Alert(json.loads(j_3))])
createOutput([g1, g2])

print('Change order of three alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1))])
createOutput([g1, g2])

print('Change value A in one alert')
json_1 = json.loads(j_1)
json_1['A'] = 'x'
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
g2 = Group()
g2.add_to_group([Alert(json_1), Alert(json.loads(j_2)), Alert(json.loads(j_3))])
createOutput([g1, g2])

print('First group has more alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_2))])
createOutput([g1, g2])

print('Second group has more alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_1))])
createOutput([g1, g2])

base_4 = '{"A": "a"}'
j_4 = '{"B": "b"}'
j_5 = '{"C": "c"}'
j_6 = '{"D": "d"}'

print('Bag of alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_4)), Alert(json.loads(base_1)), Alert(json.loads(base_1)), Alert(json.loads(base_4))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(base_1))])
createOutput_bag([g1, g2])

print('Bag of alerts different values')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_4)), Alert(json.loads(base_1)), Alert(json.loads(base_1)), Alert(json.loads(base_4))])
g2 = Group()
j_1_modified = json.loads(j_1)
j_1_modified['A'] = 'x'
g2.add_to_group([Alert(j_1_modified), Alert(j_1_modified), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(j_1_modified), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(j_1_modified), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(base_1))])
createOutput_bag([g1, g2])

print('Different lengths bag of alerts')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4))])
g2 = Group()
g2.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4))])
g3 = Group()
g3.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(base_4))])
g4 = Group()
g4.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(j_4))])
g5 = Group()
g5.add_to_group([Alert(json.loads(j_5))])
createOutput_bag([g1, g2, g3, g4, g5])

print('Merge by alignment strategy')
g1 = Group()
g1.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(j_5)), Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(j_5))])
g2 = Group()
g2.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(j_5)), Alert(json.loads(base_4)), Alert(json.loads(j_5)), Alert(json.loads(j_4))])
g3 = Group()
g3.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(j_5)), Alert(json.loads(j_4)), Alert(json.loads(j_5)), Alert(json.loads(j_4)), Alert(json.loads(j_6))])
g4 = Group()
g4.add_to_group([Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(j_5)), Alert(json.loads(base_4)), Alert(json.loads(j_5))])
createOutput_alignment([g1, g2, g3, g4])

j15 = """
{
  "A": "a1",
  "B": "b1",
  "C": "c1",
  "D": "d1"
}
"""

j16 = """
{
  "A": "a1",
  "B": "b2",
  "C": "c2"
}
"""

j17 = """
{
  "A": "a1",
  "B": "b1",
  "C": "c3"
}
"""

j18 = """
{
  "A": "a",
  "B": "b1",
  "C": ["c1", "c2"],
  "D": {
    "D1": "d1",
    "D2": "d2"
  },
  "E": "e2",
  "F": "f4",
  "G": "g8"
}"""

print('Sample for presentation')
g1 = Group()
g1.add_to_group([Alert(json.loads(j15)), Alert(json.loads(j16)), Alert(json.loads(j17)), Alert(json.loads(j17))])
g2 = Group()
g2.add_to_group([Alert(json.loads(j16)), Alert(json.loads(j17)), Alert(json.loads(j15))])
g3 = Group()
g3.add_to_group([Alert(json.loads(j15)), Alert(json.loads(j15)), Alert(json.loads(j18))])
createOutput([g1, g2, g3], 0.2)
