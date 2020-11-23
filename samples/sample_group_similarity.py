from similarity import similarity
import json
from merging.objects import Wildcard
from merging.objects import Mergelist
from preprocessing.objects import Alert
from clustering.objects import Group

def createOutput(alerts_a, alerts_b, early_stopping_threshold=0.0, strategy='best', alignment_weight=0.05):
  string = 'Group1 = '
  group_a = Group()
  for alert in alerts_a:
    string += ' ' + str(alert.d) + '\n'
    group_a.add_to_group(alert)
  group_a.create_bag_of_alerts(0.9, None, 0.0, 0.0)
  string += 'Group2 = '
  group_b = Group()
  for alert in alerts_b:
    string += ' ' + str(alert.d) + '\n'
    group_b.add_to_group(alert)
  group_b.create_bag_of_alerts(0.9, None, 0.0, 0.0)
  print(string)
  print('Similarity = ' + str(similarity.get_group_similarity(group_a, group_b, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy=strategy)) + ' (' + str(similarity.get_group_similarity(group_b, group_a, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy=strategy)) + ')')
  print('BAG Similarity = ' + str(similarity.get_group_similarity(group_a, group_b, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy='bag')) + ' (' + str(similarity.get_group_similarity(group_b, group_a, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy='bag')) + ')')
  print('')

def createOutputGroup(group_a, group_b, early_stopping_threshold=0.0, strategy='best', alignment_weight=0.05):
  string = 'Group1 = '
  string += str(group_a)
  string += 'Group2 = '
  string += str(group_b)
  print(string)
  print('Similarity = ' + str(similarity.get_group_similarity(group_a, group_b, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy=strategy)) + ' (' + str(similarity.get_group_similarity(group_b, group_a, early_stopping_threshold=early_stopping_threshold, w=None, min_alert_match_similarity=0.0, alignment_weight=alignment_weight, strategy=strategy)) + ')')
  print('')

def add_alert_to_group(alert, group, times):
  group.bag_of_alerts[alert] = 1
  for i in range(times-1):
    group.alerts.append(Alert(alert.d))
    group.merge_seq.append(Alert(alert.d))
    group.bag_of_alerts[alert] += 1

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
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3))])

print('Change order of two alerts')
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_2)), Alert(json.loads(j_1)), Alert(json.loads(j_3))])

print('Change order of three alerts')
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1))])

print('Change value A in one alert')
json_1 = json.loads(j_1)
json_1['A'] = 'x'
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json_1), Alert(json.loads(j_2)), Alert(json.loads(j_3))])

print('Different amounts of alerts')
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_1)), Alert(json.loads(j_3))])

print('Early stopping group size')
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_1))], 0.8)

j_4 =  """
{
  "A": "a3",
  "B": 1,
  "C": [
    "x",
    2
  ],
  "D": {
    "D1": false,
    "D2": [
      "x",
      "y",
      "z"
    ]
  }
}"""

print('Early stopping alert matching')
createOutput([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))], [Alert(json.loads(j_4)), Alert(json.loads(j_4)), Alert(json.loads(j_4))], 0.8)

j_5 = '{"A": "a"}'
j_6 = '{"B": "b"}'
j_7 = '{"C": "c"}'
j_8 = '{"D": "d"}'

print('Change order of repeating alerts')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_6)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6))])

print('Change frequency of repeating alerts')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6))])

print('Change order of repeating alerts bag')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_6)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6))], strategy='bag')

print('Change frequency of repeating alerts bag')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert
(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6))], strategy='bag')

print('Different amounts of alerts bag')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert
(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6)), Alert(json.loads(j_6))], strategy='bag')

print('Same order of repeating alerts without alignment')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], strategy='bag', alignment_weight=0.0)

print('Change order of repeating alerts without alignment')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_6)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6))], strategy='bag', alignment_weight=0.0)

print('Change frequency of repeating alerts without alignment')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6))], strategy='bag', alignment_weight=0.0)

print('Different amounts of alerts without alignment')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6)), Alert(json.loads(j_6))], strategy='bag', alignment_weight=0.0)

print('New alert type without alignment')
createOutput([Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_7)), Alert(json.loads(j_5)), Alert(json.loads(j_6)), Alert(json.loads(j_5))], [Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_5)), Alert(json.loads(j_7)), Alert(json.loads(j_7)), Alert(json.loads(j_6)), Alert(json.loads(j_6)), Alert(json.loads(j_8))], strategy='bag', alignment_weight=0.0)

print('Change large frequency bag')
g_8_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_8_a, 1000)
add_alert_to_group(Alert(json.loads(j_6)), g_8_a, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_8_a, 10)
g_8_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_8_b, 999)
add_alert_to_group(Alert(json.loads(j_6)), g_8_b, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_8_b, 10)
createOutputGroup(g_8_a, g_8_b, strategy = 'bag')

print('Change small frequency bag')
g_9_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_9_a, 1000)
add_alert_to_group(Alert(json.loads(j_6)), g_9_a, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_9_a, 10)
g_9_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_9_b, 1000)
add_alert_to_group(Alert(json.loads(j_6)), g_9_b, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_9_b, 9)
createOutputGroup(g_9_a, g_9_b, strategy = 'bag')

print('Similarity to merged bag missing alert')
g_10_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_10_a, 1000)
for i in range(95):
  g_10_a.alerts.append(Alert(json.loads(j_6)))
g_10_a.bag_of_alerts[Alert(json.loads(j_6))] = (90, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_10_a, 10)
g_10_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_10_b, 1000)
add_alert_to_group(Alert(json.loads(j_7)), g_10_b, 10)
createOutputGroup(g_10_a, g_10_b, strategy = 'bag')

print('Similarity to merged bag within limits')
g_11_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_11_a, 1000)
for i in range(95):
  g_11_a.alerts.append(Alert(json.loads(j_6)))
g_11_a.bag_of_alerts[Alert(json.loads(j_6))] = (90, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_11_a, 10)
g_11_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_11_b, 1000)
add_alert_to_group(Alert(json.loads(j_6)), g_11_b, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_11_b, 10)
createOutputGroup(g_11_a, g_11_b, strategy = 'bag')

print('Similarity to merged bag outside limits')
g_12_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_12_a, 1000)
for i in range(85):
  g_12_a.alerts.append(Alert(json.loads(j_6)))
g_12_a.bag_of_alerts[Alert(json.loads(j_6))] = (80, 90)
add_alert_to_group(Alert(json.loads(j_7)), g_12_a, 10)
g_12_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_12_b, 1000)
add_alert_to_group(Alert(json.loads(j_6)), g_12_b, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_12_b, 10)
createOutputGroup(g_12_a, g_12_b, strategy = 'bag')

print('Similarity two merged bags within limits')
g_13_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_13_a, 1000)
for i in range(95):
  g_13_a.alerts.append(Alert(json.loads(j_6)))
g_13_a.bag_of_alerts[Alert(json.loads(j_6))] = (90, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_13_a, 10)
g_13_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_13_b, 1000)
for i in range(90):
  g_13_b.alerts.append(Alert(json.loads(j_6)))
g_13_b.bag_of_alerts[Alert(json.loads(j_6))] = (85, 95)
add_alert_to_group(Alert(json.loads(j_7)), g_13_b, 10)
createOutputGroup(g_13_a, g_13_b, strategy = 'bag')

print('Similarity two merged bags outside limits')
g_14_a = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_14_a, 1000)
for i in range(95):
  g_14_a.alerts.append(Alert(json.loads(j_6)))
g_14_a.bag_of_alerts[Alert(json.loads(j_6))] = (90, 100)
add_alert_to_group(Alert(json.loads(j_7)), g_14_a, 10)
g_14_b = Group()
add_alert_to_group(Alert(json.loads(j_5)), g_14_b, 1000)
for i in range(80):
  g_14_b.alerts.append(Alert(json.loads(j_6)))
g_14_b.bag_of_alerts[Alert(json.loads(j_6))] = (75, 85)
add_alert_to_group(Alert(json.loads(j_7)), g_14_b, 10)
createOutputGroup(g_14_a, g_14_b, strategy = 'bag')

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

j19 =  """
{
  "A": "a",
  "B": "b2",
  "C": ["c1"],
  "D": {
    "D1": "d1"
  },
  "E": "replace_with_mergelist",
  "F": "replace_with_mergelist",
  "G": "replace_with_wildcard"
}"""

print('Sample for presentation')
j19_json = json.loads(j19)
j19_json["E"] = Mergelist(["e1", "e2", "e3"])
j19_json["F"] = Mergelist(["f1", "f2", "f3"])
j19_json["G"] = Wildcard()
createOutput([Alert(json.loads(j18)), Alert(json.loads(j15)), Alert(json.loads(j17))], [Alert(json.loads(j17)), Alert(j19_json), Alert(json.loads(j16)), Alert(json.loads(j16))], alignment_weight=0.0)

print('Sample for presentation bag')
g_15 = Group()
add_alert_to_group(Alert(json.loads(j18)), g_15, 1000)
for i in range(95):
  g_15.alerts.append(Alert(json.loads(j16)))
g_15.bag_of_alerts[Alert(json.loads(j16))] = (90, 100)
for i in range(9):
  g_15.alerts.append(Alert(json.loads(j17)))
g_15.bag_of_alerts[Alert(json.loads(j17))] = (9, 11)
g_16 = Group()
add_alert_to_group(Alert(j19_json), g_16, 1050)
for i in range(80):
  g_16.alerts.append(Alert(json.loads(j16)))
g_16.bag_of_alerts[Alert(json.loads(j16))] = (75, 85)
add_alert_to_group(Alert(json.loads(j17)), g_16, 10)
add_alert_to_group(Alert(json.loads(j15)), g_16, 1)
createOutputGroup(g_15, g_16, strategy = 'bag', alignment_weight=0.0)
