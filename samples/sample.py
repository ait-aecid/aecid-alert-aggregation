from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase

# files = [[system_A_ids_1, system_A_ids_2], [system_B_ids_1, system_B_ids_2, system_B_ids_3, ...], ...]
# For a single file, just use files = [['path_to_file']]
#files = [['data/ossec/ossec_cup.json'], ['data/ossec/ossec_onion.json'], ['data/ossec/ossec_insect.json']]
#files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]
#files = [['data/test/test_cup.txt'], ['data/test/test_onion.txt'], ['data/test/test_insect.txt'], ['data/test/test_spiral.txt']]
files = [['data/patent/test_cup.txt'], ['data/patent/test_spiral.txt']]
#files = [['data/aminer/exim_cup.txt'], ['data/aminer/exim_insect.txt'], ['data/aminer/exim_spiral.txt']]
#files = [['data/aminer/nmap_cup.txt'], ['data/aminer/nmap_insect.txt'], ['data/aminer/nmap_spiral.txt'], ['data/aminer/nmap_onion.txt']]
#files = [['data/aminer/sample.txt']]
input_type = 'aminer' # One of 'aminer', 'ossec', or 'idmef'. If None, automatically selects correct parser based on input file directory
deltas = [1, 10, 50, 100] # [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50] # seconds
thresholds = [0.5]
max_val_limit = 2
min_key_occurrence = 0.1
min_val_occurrence = 0.1
alignment_weight = 0.1
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
min_alert_match_similarity = None # Set to None to use threshold

groups_dict = read_input.read_input(files, deltas, input_type)
for threshold in thresholds:
  min_alert_match_similarity_val = min_alert_match_similarity
  if min_alert_match_similarity_val is None:
    min_alert_match_similarity_val = threshold

  kb = KnowledgeBase()
  mam = MetaAlertManager(kb)

  for file_group_index, delta_dicts in groups_dict.items():
    print('Now processing file ' + str(file_group_index + 1) + '/' + str(len(files)) + '...')
    for delta, groups in delta_dicts.items():
      print(' Processing groups with delta=' + str(delta))
      for group in groups:
        #print(group)
        label.label_group(group)
        group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
        new_meta_alert_generated = mam.add_to_meta_alerts(group, delta, threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, w=w, alignment_weight=alignment_weight)
        kb.add_group_delta(group, delta)
        new_meta_alert_info = ''
        if new_meta_alert_generated is True:
          new_meta_alert_info = ' New meta-alert generated.'
        print('  Processed group ' + str(groups.index(group) + 1) + '/' + str(len(groups)) + ' with ' + str(len(group.alerts)) + ' alerts.' + new_meta_alert_info)

  #print(mam.get_json_representation())
