from merging.merge import merge_group, merge_bag
import json
from merging.objects import Wildcard
from merging.objects import Mergelist
from preprocessing.objects import Alert
from clustering.objects import Group
from merging.objects import KnowledgeBase

def createOutput(groups, labels, max_val_limit=1000):
  kb = KnowledgeBase()
  i = 0
  for group in groups:
    print('Group ' + str(i))
    i += 1
    for alert in group.alerts:
      print(alert.d)
    kb.add_group_delta(group, 1)
  print(kb.hierarchical_clustering(labels, max_val_limit=max_val_limit))
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

base_4 = '{"A": "a"}'
j_4 = '{"B": "b"}'
j_5 = '{"C": "c"}'

j_6 =  """
{
  "A": "y",
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

print('Sample')
labels = {}
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3))])
labels[g1] = 'g1'
g2 = Group()
g2.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3))])
labels[g2] = 'g2'
g3 = Group()
g3.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_3)), Alert(json.loads(base_1)), Alert(json.loads(base_2)), Alert(json.loads(base_4)), Alert(json.loads(base_1)), Alert(json.loads(base_1)), Alert(json.loads(base_4))])
labels[g3] = 'g3'
g4 = Group()
g4.add_to_group([Alert(json.loads(j_1)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(j_1)), Alert(json.loads(j_2)), Alert(json.loads(j_3)), Alert(json.loads(base_4)), Alert(json.loads(base_4)), Alert(json.loads(j_4)), Alert(json.loads(base_1))])
labels[g4] = 'g4'
g5 = Group()
g5.add_to_group([Alert(json.loads(base_1)), Alert(json.loads(base_2))])
labels[g5] = 'g5'
g6 = Group()
g6.add_to_group([Alert(json.loads(base_1))])
labels[g6] = 'g6'
g7 = Group()
g7.add_to_group([Alert(json.loads(base_2))])
labels[g7] = 'g7'
g8 = Group()
g8.add_to_group([Alert(json.loads(base_3))])
labels[g8] = 'g8'
createOutput([g1, g2, g3, g4, g5, g6, g7, g8], labels)

print('Similarity increases after merge')
labels = {}
g1 = Group()
g1.add_to_group([Alert(json.loads(base_1))])
labels[g1] = 'g1'
g2 = Group()
g2.add_to_group([Alert(json.loads(base_2))])
labels[g2] = 'g2'
g3 = Group()
g3.add_to_group([Alert(json.loads(base_3))])
labels[g3] = 'g3'
g4 = Group()
g4.add_to_group([Alert(json.loads(j_3))])
labels[g4] = 'g4'
g5 = Group()
g5.add_to_group([Alert(json.loads(j_6))])
labels[g5] = 'g5'
g6 = Group()
g6.add_to_group([Alert(json.loads(j_6)), Alert(json.loads(j_6))])
labels[g6] = 'g6'
g7 = Group()
g7.add_to_group([Alert(json.loads(j_6)), Alert(json.loads(j_6)), Alert(json.loads(j_6))])
labels[g7] = 'g7'
createOutput([g1, g2, g3, g4, g5, g6, g7], labels, 2)
