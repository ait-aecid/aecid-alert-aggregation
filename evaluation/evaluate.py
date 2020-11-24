from preprocessing import label
from preprocessing import read_input
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase
import time

files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]
input_type = None
deltas = [0.5, 5, 50] # [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 500] # seconds
thresholds = [0.2, 0.3, 0.4] # [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
max_val_limit = 10
min_key_occurrence = 0.1
min_val_occurrence = 0.1
alignment_weight = 0.1
max_groups_per_meta_alert = 25
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
min_alert_match_similarity = None # Set to None to use threshold

with open('data/out/evaluation/evaluation.txt', 'w') as out, open('data/out/evaluation/number_groups.txt', 'w') as num_groups_out:
  out.write('threshold,delta,attack,tp,fp,fn,tn,tpr,fpr,prec,f1,groups,meta_alerts,reduction,groups_alerts,meta_alerts_alerts,reduction_alerts,avg_ratio,runtime\n')
  num_groups_out.write('threshold,delta,file,num_groups\n')
  labels = ['nmap', 'nikto', 'vrfy', 'hydra', 'upload', 'exploit', 'non-attack', 'multiple']
  groups_dict = read_input.read_input(files, deltas, input_type)
  for threshold in thresholds:
    min_alert_match_similarity_val = min_alert_match_similarity
    if min_alert_match_similarity_val is None:
      min_alert_match_similarity_val = threshold

    kb = KnowledgeBase(max_groups_per_meta_alert, evaluate=True)
    mam = MetaAlertManager(kb)

    runtimes = {}
    for delta in deltas:
      runtimes[delta] = 0.0

    for file_group_index, delta_dicts in groups_dict.items():
      print('Now analyzing threshold ' + str(threshold) + ', file #' + str(file_group_index))
      for delta, groups in delta_dicts.items():
        num_groups_out.write(str(threshold) + ',' + str(delta) + ',' + str(files[file_group_index][0].split('.')[0].split('/')[-1]) + ',' + str(len(groups)) + '\n')
        for group in groups:
          label.label_group(group)
          start = time.time()
          group.create_bag_of_alerts(min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
          mam.add_to_meta_alerts(group, delta, threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, w=w, alignment_weight=alignment_weight)
          kb.add_group_delta(group, delta)
          runtimes[delta] += time.time() - start

    for delta, groups in kb.delta_dict.items():
      tp = {}
      fp = {}
      tn = {}
      fn = {}
      tpr = {}
      fpr = {}
      prec = {}
      f1 = {}
      for l in labels:
        tp[l] = 0
        fp[l] = 0
        tn[l] = 0
        fn[l] = 0
      for group_outer in groups:
        for group_inner in kb.delta_dict[delta]:
          if group_outer == group_inner:
            # Only consider pairs of different groups
            continue
          outer_label = str(list(group_outer.attacks)[0])
          if len(group_outer.attacks) > 1:
            outer_label = 'multiple'
          inner_label = str(list(group_inner.attacks)[0])
          if len(group_inner.attacks) > 1:
            inner_label = 'multiple'
          if group_outer.meta_alert == group_inner.meta_alert:
            if outer_label == inner_label:
              tp[outer_label] += 1
            else:
              fp[outer_label] += 1
          else:
            if group_outer.attacks == group_inner.attacks:
              fn[outer_label] += 1
            else:
              tn[outer_label] += 1
      for l in labels:
        # Note: Sum of tp, fp, tn, fn should be #groups * (#groups - 1), since all pairs are considered twice (a, b) <=> (b, a)
        if tp[l] == 0 and fn[l] == 0:
          tpr[l] = 0.0
        else:
          tpr[l] = tp[l] / (tp[l] + fn[l]) # tpr = recall
        if fp[l] == 0 and tn[l] == 0:
          fpr[l] = 0
        else:
          fpr[l] = fp[l] / (fp[l] + tn[l])
        if tp[l] == 0 and fp[l] == 0:
          prec[l] = 0.0
        else:
          prec[l] = tp[l] / (tp[l] + fp[l])
        if tp[l] == 0 and fp[l] == 0 and fn[l] == 0:
          f1[l] = 0
        else:
          f1[l] = tp[l] / (tp[l] + 0.5 * (fp[l] + fn[l]))

        total_alerts = sum([len(g.alerts) for g in groups])
        total_meta_alerts_alerts = sum([len(m.alert_group.alerts) for m in mam.meta_alerts[delta]])
        avg_num_ratios = []
        for m in mam.meta_alerts[delta]:
          num_alerts_in_m = len(m.alert_group.alerts)
          num_alerts_allocated_to_m = sum([len(g.alerts) for g in kb.meta_alert_dict_unlimited[m]])
          avg_num_ratios.append(1 - num_alerts_in_m / num_alerts_allocated_to_m)
        out.write(str(threshold) + ',' + str(delta) + ',' + str(l) + ',' + str(tp[l]) + ',' + str(fp[l]) + ',' + str(fn[l]) + ',' + str(tn[l]) + ',' + str(tpr[l]) + ',' + str(fpr[l]) + ',' + str(prec[l]) + ',' + str(f1[l]) + ',' + str(len(groups)) + ',' + str(len(mam.meta_alerts[delta])) + ',' + str(1 - len(mam.meta_alerts[delta]) / (len(groups))) + ',' + str(total_alerts) + ',' + str(total_meta_alerts_alerts) + ',' + str(1 - total_meta_alerts_alerts / total_alerts) + ',' + str(sum(avg_num_ratios) / len(avg_num_ratios)) + ',' + str(runtimes[delta]) + '\n')

