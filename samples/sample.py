from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase

files = [['data/sample/test_cup.txt'], ['data/sample/test_spiral.txt']]
input_type = 'aminer' 
deltas = [1, 10, 50, 100] # seconds
threshold = 0.5
max_val_limit = 2
min_key_occurrence = 0.1
min_val_occurrence = 0.1
alignment_weight = 0.1
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
min_alert_match_similarity = None # Set to None to use threshold

groups_dict = read_input.read_input(files, deltas, input_type)
with open('data/out/sample/meta_alerts.txt', 'w') as out:
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
        label.label_group(group)
        group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
        new_meta_alert_generated = mam.add_to_meta_alerts(group, delta, threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, w=w, alignment_weight=alignment_weight)
        kb.add_group_delta(group, delta)
        new_meta_alert_info = ''
        if new_meta_alert_generated is True:
          new_meta_alert_info = ' New meta-alert generated.'
        print('  Processed group ' + str(groups.index(group) + 1) + '/' + str(len(groups)) + ' with ' + str(len(group.alerts)) + ' alerts.' + new_meta_alert_info)

  print('\nResults:')
  for delta, meta_alerts in mam.meta_alerts.items():
    print(' delta = ' + str(delta) + ': ' + str(len(meta_alerts)) + ' meta-alerts generated')

  out.write(mam.get_json_representation())
  print('\nMeta-alerts are stored in data/out/sample/meta_alerts.txt')

  #if aggregate_config.output_alerts is True:
  #  out_alerts.write(kb.get_json_representation())
  #  print('\nAlerts are stored in ' + str(aggregate_config.output_alerts_dir))
