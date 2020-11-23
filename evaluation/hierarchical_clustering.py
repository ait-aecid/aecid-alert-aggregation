from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase

files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]
input_type = None
deltas = [10] # seconds
max_val_limit = 10
min_key_occurrence = 0.1
min_val_occurrence = 0.1
alignment_weight = 0.1
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
omit_false_alarms = True
min_alert_match_similarity_val = 0.3

groups_dict = read_input.read_input(files, deltas, input_type)

kb = KnowledgeBase()
mam = MetaAlertManager(kb)

labels = {}
for file_group_index, delta_dicts in groups_dict.items():
  for delta, groups in delta_dicts.items():
    omitted = 0
    for group in groups:
      labels[group] = label.label_group(group) + str(group.id)
      if omit_false_alarms is True and '-non-attack' in labels[group]: # Omit false alarms
        omitted += 1
        continue
      group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
      kb.add_group_delta(group, delta)
  print('Omitted ' + str(omitted) + ' false positives, ' + str(len(groups) - omitted) + ' remain.')

code = kb.hierarchical_clustering(labels=labels, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, early_stopping_threshold=0.0, w=None, alignment_weight=alignment_weight, bag_limit=2000)

with open('data/out/hierarchical/hierarchical_clustering.R', 'w') as out:
  out.write('library(data.tree)\nlibrary(yaml)\nlibrary(ggdendro)\nlibrary(treemap)\nlibrary(dendextend)\n\n')
  out.write(code)
