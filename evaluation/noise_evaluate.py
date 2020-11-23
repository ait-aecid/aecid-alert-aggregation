from preprocessing import label
from preprocessing import read_input
from clustering import time_delta_group
from similarity import similarity
from merging.objects import MetaAlert, MetaAlertManager, KnowledgeBase

files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]
input_type = None
deltas = [5] # seconds
threshold = 0.3
max_val_limit = 10
min_key_occurrence = 0.1
min_val_occurrence = 0.1
bag_limit = 2000
alignment_weight = 0.1
max_groups_per_meta_alert = 25
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0}
train_only_same_labels = True
min_alert_match_similarity = None # Set to None to use threshold
min_group_match_similarity = 0.1

noises = [0.0, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 500] # Avg number of false alarms per minute

with open('data/out/noise/sim_list.txt', 'w') as sim_out, open('data/out/noise/noise.txt', 'w') as cross_corr, open('data/out/noise/reductions.txt', 'w') as reduct, open('data/out/noise/noise_number_groups.txt', 'w') as num_groups_out:
  labels = ['nmap', 'nikto', 'vrfy', 'hydra', 'upload', 'exploit', 'non-attack', 'multiple', 'noise']
  cross_corr.write('threshold,delta,attack,noise,tp,fp,fn,tn,tpr,fpr,prec,f1\n')
  sim_out.write('threshold,delta,label,prediction,correct,group_id,similarity\n')
  reduct.write('threshold,delta,groups,meta_alerts,group_reduction,alerts,meta_alerts_alerts,alert_reduction\n')
  num_groups_out.write('threshold,delta,file,num_groups,noise\n')
  for noise in noises:
    groups_dict = read_input.read_input(files, deltas, input_type, noise)

    min_alert_match_similarity_val = min_alert_match_similarity
    if min_alert_match_similarity_val is None:
      min_alert_match_similarity_val = threshold

    # Initialize confusion matrix with zeros
    confusion_matrix = {} # confusion_matrix[<actual_class>][<predicted_class>] = #count
    similarities_matrix = {} # similarities_matrix[<actual_class>][<predicted_class>] = [sim_1, sim_2, ...]
    for lab in labels:
      confusion_matrix[lab] = {}
      similarities_matrix[lab] = {}
      for label_inner in labels:
        confusion_matrix[lab][label_inner] = 0 
        similarities_matrix[lab][label_inner] = []

    tp = {}
    fp = {}
    tn = {}
    fn = {}
    total_alerts = {}
    total_meta_alerts_alerts = {} # Alerts within meta_alert groups
    total_groups = {}
    total_meta_alerts = {}
    for delta in deltas:
      tp[delta] = {}
      fp[delta] = {}
      tn[delta] = {}
      fn[delta] = {}
      total_alerts[delta] = 0
      total_meta_alerts_alerts[delta] = 0
      total_groups[delta] = 0
      total_meta_alerts[delta] = 0
      for lab in labels:
        tp[delta][lab] = 0
        fp[delta][lab] = 0
        tn[delta][lab] = 0
        fn[delta][lab] = 0

    for test_data in range(len(files)):
      print('Now testing files #' + str(test_data) + ' with noise ' + str(noise))
      kb = KnowledgeBase(max_groups_per_meta_alert)
      mam = MetaAlertManager(kb)

      # TRAINING
      for file_group_index, delta_dicts in groups_dict.items():
        if file_group_index == test_data:
          # Leave out test file from learning
          continue
        for delta, groups in delta_dicts.items():
          if noise is None:
            num_groups_out.write(str(threshold) + ',' + str(delta) + ',' + str(files[file_group_index][0].split('.')[0].split('/')[-1]) + ',' + str(len(groups)) + ',0.0' + '\n')
          else:
            num_groups_out.write(str(threshold) + ',' + str(delta) + ',' + str(files[file_group_index][0].split('.')[0].split('/')[-1]) + ',' + str(len(groups)) + ',' + str(noise) + '\n')
          for group in groups:
            label.label_group(group)
            force_label = None
            if train_only_same_labels is True:
              force_label = group.attacks # Only allow meta alert generation for alerts with same label
            mam.add_to_meta_alerts(group, delta, threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, w=w, alignment_weight=alignment_weight, force_label=force_label)
            kb.add_group_delta(group, delta)
  
      meta_alert_counter = {}
      for delta, meta_alerts in mam.meta_alerts.items():
        for meta_alert in meta_alerts:
          if frozenset(meta_alert.alert_group.attacks) not in meta_alert_counter:
            meta_alert_counter[frozenset(meta_alert.alert_group.attacks)] = 1
          else:
            meta_alert_counter[frozenset(meta_alert.alert_group.attacks)] += 1
      
      # TESTING
      for file_group_index, delta_dicts in groups_dict.items():
        if file_group_index != test_data:
          # Leave out all training files from testing
          continue
        for delta, groups in delta_dicts.items():
          total_alerts[delta] += sum([len(g.alerts) for g in groups])
          total_groups[delta] += len(groups)
          used_meta_alerts = set()

          for group in groups:
            label.label_group(group)
            meta_alert, similarity = mam.get_most_similar_meta_alert(group, delta, threshold, min_alert_match_similarity=min_alert_match_similarity_val, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, bag_limit=bag_limit, w=w, alignment_weight=alignment_weight)
            meta_attack_labels = []
            for g in kb.get_groups(meta_alert):
              # Get all group labels that are associated with the most similar meta alert
              meta_attack_labels.extend(g.attacks)

            if len(group.attacks) > 1:
              group_attacks = 'multiple'
            else:
              group_attacks = list(group.attacks)[0]

            if similarity >= min_group_match_similarity:
              used_meta_alerts.add(meta_alert)

            if similarity < min_group_match_similarity:
              # False positive in this context means that it cannot be allocated to any known class and is therefore a false positive from the ids
              meta_attacks = 'non-attack'
            elif len(meta_alert.alert_group.attacks) > 1:
              meta_attacks = 'multiple'
            else:
              meta_attacks = list(meta_alert.alert_group.attacks)[0]
            confusion_matrix[str(group_attacks)][str(meta_attacks)] += 1
            similarities_matrix[str(group_attacks)][str(meta_attacks)].append(similarity)
            if group_attacks == meta_attacks:
              tp[delta][str(group_attacks)] += 1
              for l in labels:
                if l != str(group_attacks):
                  tn[delta][l] += 1
            else:
              fn[delta][str(group_attacks)] += 1
              fp[delta][str(meta_attacks)] += 1
              for l in labels:
                if l != str(group_attacks) and l != str(meta_attacks):
                  tn[delta][l] += 1
            sim_out.write(str(threshold) + ',' + str(delta) + ',' + str(group_attacks) + ',' + str(meta_attacks) + ',' + str(group.attacks == meta_alert.alert_group.attacks) + ',' + str(group.id) + ',' + str(similarity) + '\n')
          total_meta_alerts_alerts[delta] += sum([len(m.alert_group.alerts) for m in used_meta_alerts])
          total_meta_alerts[delta] += len(used_meta_alerts)

    for delta in deltas:
      reduct.write(str(threshold) + ',' + str(delta) + ',' + str(total_groups[delta]) + ',' + str(total_meta_alerts[delta]) + ',' + str(1 - total_meta_alerts[delta] / total_groups[delta]) + ',' + str(total_alerts[delta]) + ',' + str(total_meta_alerts_alerts[delta]) + ',' + str(1 - total_meta_alerts_alerts[delta] / total_alerts[delta]) + '\n')
      for l in labels:
        if tp[delta][l] == 0 and fn[delta][l] == 0:
          tpr = 0
        else:
          tpr = tp[delta][l] / (tp[delta][l] + fn[delta][l]) # tpr = recall
        if fp[delta][l] == 0 and tn[delta][l] == 0:
          fpr = 0
        else:
          fpr = fp[delta][l] / (fp[delta][l] + tn[delta][l])
        if tp[delta][l] == 0 and fp[delta][l] == 0:
          prec = 0.0
        else:
          prec = tp[delta][l] / (tp[delta][l] + fp[delta][l])
        if tp[delta][l] == 0 and fp[delta][l] + fn[delta][l] == 0:
          f1 = 0.0
        else:
          f1 = tp[delta][l] / (tp[delta][l] + 0.5 * (fp[delta][l] + fn[delta][l]))

        cross_corr.write(str(threshold) + ',' + str(delta) + ',' + str(l) + ',' + str(noise) + ',' + str(tp[delta][l]) + ',' + str(fp[delta][l]) + ',' + str(fn[delta][l]) + ',' + str(tn[delta][l]) + ',' + str(tpr) + ',' + str(fpr) + ',' + str(prec) + ',' + str(f1) + '\n')

    # rows = actual, columns = prediction
    with open('data/out/noise/attack_similarities_matrix_' + str(threshold).replace('.', '_') + '.txt', 'w') as similarities_out:
      similarities_str = ''
      for attack in similarities_matrix:
        similarities_str += str(attack) + ','
      similarities_str = similarities_str[:-1] + '\n'
      for attack in similarities_matrix:
        for meta_attack in similarities_matrix[attack]:
          if len(similarities_matrix[attack][meta_attack]) != 0:
            similarities_str += str(sum(similarities_matrix[attack][meta_attack]) / len(similarities_matrix[attack][meta_attack])) + ','
          else:
            similarities_str += '-1,'
        similarities_str = similarities_str[:-1] + '\n'
      similarities_out.write(similarities_str)

    with open('data/out/noise/confusion_matrix_' + str(threshold).replace('.', '_') + '.txt', 'w') as confusion_out:
      confusion_str = ''
      for attack in confusion_matrix:
        confusion_str += str(attack) + ','
      confusion_str = confusion_str[:-1] + '\n'
      for attack in confusion_matrix:
        for meta_attack in confusion_matrix[attack]:
          confusion_str += str(confusion_matrix[attack][meta_attack]) + ','
        confusion_str = confusion_str[:-1] + '\n'
      confusion_out.write(confusion_str)

