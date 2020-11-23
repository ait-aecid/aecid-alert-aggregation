from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase

files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]
input_type = None
deltas = [1] # seconds
max_val_limit = 10
min_key_occurrence = 0.1
min_val_occurrence = 0.1
alignment_weight = 0.1
bag_limit = 2000
omit_fp = True
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
min_alert_match_similarity_val = 0.2

groups_dict = read_input.read_input(files, deltas, input_type)

group_list = []
for file_group_index, delta_dicts in groups_dict.items():
  for delta, groups in delta_dicts.items():
    for group in groups:
      label.label_group(group)
      if omit_fp is False or 'non-attack' not in group.attacks:
        group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
        group_list.append(group)
  
meta_info = 'group_id,class,file\n'
for group in group_list:
  if len(group.attacks) != 1:
    print('Incorrect group labeling!')
    print(group.attacks)
  meta_info += str(group.id) + ',' + str(list(group.attacks)[0]) + ',' + str(group.files[0].split('_')[1].split('.')[0]) + '\n'
with open('data/out/mds/mds_sim_matrix_meta.txt', 'w') as out:
  out.write(meta_info)

similarity_matrix = ''
total = len(group_list) * len(group_list)
current = 1
for group in group_list:
  for group_inner in group_list:
    print(str(current) + '/' + str(total) + '...')
    current += 1
    if len(group.alerts) * len(group_inner.alerts) > bag_limit:
      s = similarity.get_group_similarity(group, group_inner, w=w, min_alert_match_similarity=min_alert_match_similarity_val, alignment_weight=alignment_weight, strategy='bag')
    else:
      s = similarity.get_group_similarity(group, group_inner, w=w, min_alert_match_similarity=min_alert_match_similarity_val, alignment_weight=alignment_weight, strategy='best')
    similarity_matrix += str(s) + ','
  similarity_matrix = similarity_matrix[:-1] + '\n'
with open('data/out/mds/mds_sim_matrix.txt', 'w') as out:
  out.write(similarity_matrix)
