from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase
import aggregate_config

min_alert_match_similarity_val = aggregate_config.min_alert_match_similarity
if min_alert_match_similarity_val is None:
  min_alert_match_similarity_val = aggregate_config.threshold

groups_dict = read_input.read_input(aggregate_config.files, aggregate_config.deltas, aggregate_config.input_type, 0.0, aggregate_config.group_strategy, aggregate_config.group_type)
with open(aggregate_config.output_dir, 'w') as out, open(aggregate_config.output_alerts_dir, 'w') as out_alerts:
  kb = KnowledgeBase(aggregate_config.max_groups_per_meta_alert, aggregate_config.queue_strategy)
  mam = MetaAlertManager(kb)

  for file_group_index, delta_dicts in groups_dict.items():
    print('Now processing file ' + str(file_group_index + 1) + '/' + str(len(aggregate_config.files)) + '...')
    for delta, groups in delta_dicts.items():
      print(' Processing groups with delta = ' + str(delta))
      for group in groups:
        label.label_group(group)
        group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=aggregate_config.max_val_limit, min_key_occurrence=aggregate_config.min_key_occurrence, min_val_occurrence=aggregate_config.min_val_occurrence)
        new_meta_alert_generated, sim, meta_alert = mam.add_to_meta_alerts(group, delta, aggregate_config.threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=aggregate_config.max_val_limit, min_key_occurrence=aggregate_config.min_key_occurrence, min_val_occurrence=aggregate_config.min_val_occurrence, w=aggregate_config.w, alignment_weight=aggregate_config.alignment_weight)
        kb.add_group_delta(group, delta)
        new_meta_alert_info = ''
        if new_meta_alert_generated is True:
          new_meta_alert_info = ' New meta-alert ' + str(meta_alert.id) + ' generated. (sim=' + str(round(sim, 2)) + ')'
        else:
          new_meta_alert_info = ' Add group to meta-alert ' + str(meta_alert.id) + ' (sim=' + str(round(sim, 2)) + ') representing ' + str(meta_alert.alert_group.attacks)
        print('  Processed group ' + str(groups.index(group) + 1) + '/' + str(len(groups)) + ' from ' + str(group.attacks) + ' phase with ' + str(len(group.alerts)) + ' alerts.' + new_meta_alert_info)
  
  print('\nResults:')
  for delta, meta_alerts in mam.meta_alerts.items():
    print(' delta = ' + str(delta) + ': ' + str(len(meta_alerts)) + ' meta-alerts generated')

  out.write(mam.get_json_representation())
  print('\nMeta-alerts are stored in ' + str(aggregate_config.output_dir))

  if aggregate_config.output_alerts is True:
    out_alerts.write(kb.get_json_representation())
    print('\nAlerts are stored in ' + str(aggregate_config.output_alerts_dir))

