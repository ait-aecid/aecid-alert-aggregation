import math
from collections import Counter
from merging.objects import Mergelist
from merging.objects import Wildcard
import editdistance

def get_json_similarity(a, b, w=None):
  match, mismatch = get_dict_similarity(a, b, w)
  return match / (match + mismatch)

def get_dict_similarity(a, b, w=None):
  match = 0
  mismatch = 0
  for key in a:
    a_type = type(a[key])
    mat = 0
    mis = 0
    if key in b:
      b_type = type(b[key])
      if a_type is Wildcard or b_type is Wildcard:
        # Will match any
        mat = 1
      elif a_type is dict and b_type is dict:
        # Both are dicts, start recursion
        mat, mis = get_dict_similarity(a[key], b[key], w)
      elif a_type is dict or b_type is dict:
        # Cannot compare dict with other datatype; always mismatch
        mis = max(weight(a[key], a_type), weight(b[key], b_type))
      elif a_type is Mergelist and b_type is Mergelist:
        # Compute sum of common elements with respect to list lengths, only mismatch when no common elements
        mat, mis = get_mergelist_similarity(a[key].elements, b[key].elements)
      elif a_type is Mergelist:
        # Compute how many values of list occur in mergelist
        mat, mis = get_alert_mergelist_similarity(b[key], a[key], b_type)
      elif b_type is Mergelist:
        # Compute how many values of list occur in mergelist
        mat, mis = get_alert_mergelist_similarity(a[key], b[key], a_type)
      elif a_type is list and b_type is list:
        # Compute number of common elements in relation to number of mismatching elements
        mat, mis = get_list_similarity(a[key], b[key])
      elif a_type is list:
        # Compute number of elements in list
        if b[key] in a[key]:
          mat = 1
        else:
          mis = max(weight(a[key], a_type), weight(b[key], b_type))
      elif b_type is list:
        if a[key] in b[key]:
          mat = 1
        else:
          mis = max(weight(a[key], a_type), weight(b[key], b_type))
      elif a[key] == b[key]:
        mat = 1
      else:
        mis = 1
    else:
      mis = 0.5 + weight(a[key], a_type) # Add 0.5 because missing key is worse than mismatching value
    if w is not None and key in w:
      mat *= w[key]
      mis *= w[key]
    match += mat
    mismatch += mis
    # Debug output:
    #print(str(key) + ': mat=' + str(mat) + ', mis=' + str(mis) + '; match=' + str(match) + ', mismatch=' + str(mismatch))
  for key in b:
    # Common elements already counted as matches; only increase mismatches
    if key not in a:
      mismatch += 0.5 + weight(b[key], type(b[key])) # Add 0.5 because missing key is worse than mismatching value
  return match, mismatch

def get_list_similarity_old(a, b):
  # DEPRECATED, cannot handle nested lists
  # Lists are not assumed to be sorted; use counter to cope with duplicate elements
  counter_a = Counter(a)
  counter_b = Counter(b)
  intersection = counter_a & counter_b
  match = sum(intersection.values())
  diff = None
  if len(a) > len(b):
    diff = counter_a - counter_b
  else:
    diff = counter_b - counter_a
  mismatch = sum(diff.values())

  # Normalize so that lists counts same as value
  return match / (match + mismatch), mismatch / (match + mismatch)

def get_list_similarity(a, b):
  # Common elements vs mismatching elements
  match = 0
  mismatch = 0
  used_b = []
  for elem_a in a:
    if elem_a in b:
      used_b.append(elem_a)
      match += 1
    else:
      mismatch += 1
  for elem_b in b:
    if elem_b not in used_b:
      mismatch += 1 
      
  if match == 0 and mismatch == 0:
    return 1, 0

  # Normalize so that lists count same as value
  return match / (match + mismatch), mismatch / (match + mismatch)

def get_mergelist_similarity(merge_a, merge_b):
  # Only common elements or mismatch when all elements differ
  match = 0
  mismatch = 0
  for elem_a in merge_a:
    if elem_a in merge_b:
      match += 1
  if match == 0:
    mismatch = 1
    
  if len(merge_a) == 0 and len(merge_b) == 0:
    return 1, 0

  return match / min(len(merge_a), len(merge_b)), mismatch

def get_mergedlist_similarity(a, b):
  # Deprecated; correct method is called directly in get_json_similarity
  # Compute number of elements in merged list
  if isinstance(b, Mergelist):
    return get_alert_mergelist_similarity(a, b)
  elif isinstance(a, Mergelist):
    return get_alert_mergelist_similarity(b, a)

def get_alert_mergelist_similarity(a, merge, a_type):
  # Lists are not assumed to be ordered
  match = 0
  mismatch = 0
  if a in merge.elements:
    # Note that a could be a list and merge.elements a list of lists
    match += 1
  elif a_type is list:
    for elem_a in a:
      for merge_elem in merge.elements:
        if elem_a == merge_elem or (isinstance(merge_elem, list) and elem_a in merge_elem):
          match += 1
        else:
          mismatch += 1
  else:
    mismatch += 1

  if match == 0 and mismatch == 0:
    return 1, 0
    
  # Normalize so that lists counts same as value
  return match / (match + mismatch), mismatch / (match + mismatch)

def weight(elem, elem_type):
  # Dampen influence of large lists or dicts
  w = 0
  if (elem_type is list or elem_type is dict) and len(elem) > 0:
    w += 1 + math.log(len(elem))
  else:
    w += 1
  return w

def find_alert_matching(alerts_a, alerts_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0):
  # Returns a dictionary of alert pairs (tupels) from lists of alerts alerts_a and alerts_b sorted by their respective similarities (value of dict)
  similarities = []
  alert_pairs = []
  max_allowed_total_dist = (1 - early_stopping_threshold) * max(len(alerts_a), len(alerts_b)) # When using early stopping, this must correspond to criteria for declaring groups a match or not
  current_max_dist = abs(len(alerts_a) - len(alerts_b)) # If number of alerts are not equal, the alerts that will not find a match are counted in as contributing to the distance as perfect mismatches
  for a in alerts_a:
    # Compute highest possible overall distance given all already seen a to allow early stopping
    max_s = 0.0
    for b in alerts_b:
      s = get_json_similarity(a.d, b.d, w)
      if s >= min_alert_match_similarity:
        similarities.append(s)
        alert_pairs.append((a, b))
      if s > max_s:
        max_s = s
    current_max_dist += (1 - max_s)
    if current_max_dist > max_allowed_total_dist and early_stopping_threshold != 0.0: # Never stop when early_stopping_threshold is 0.0
      # Debug output:
      #print('Early stopping, because current max dist is ' + str(current_max_dist) + ' > ' + str(max_allowed_total_dist))
      return {}
  return {y: x for x, y in sorted(zip(similarities, alert_pairs), key=lambda pair: pair[0], reverse=True)} # key to avoid that sort takes second list into account in case first list has duplicates

def get_group_similarity_avg(group_a, group_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0, alignment_weight=0.0, partial=False):
  # Similarity is the average of all similarities of alert pairs from group_a and group_b
  s = 0.0
  for a in group_a.alerts:
    for b in group_b.alerts:
      s += get_json_similarity(a.d, b.d)
  s /= len(group_a.alerts) * len(group_b.alerts)
  return s 

def get_group_similarity_exact(group_a, group_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0, alignment_weight=0.0, partial=False):
  # Find the best alignment of alerts in group_a and group_b, resulting similarity is average of the similarities of all aligned alerts
  if min(len(group_a.alerts), len(group_b.alerts)) / max(len(group_a.alerts), len(group_b.alerts)) < early_stopping_threshold:
    # Debug output: Since highest possible similarity means a perfect match for each alert in the smaller alert list, it has to be at least threshold*max_len long to be able to achieve the required minimum similarity
    #print('Early stopping, because length ratio is ' + str(min(len(group_a.alerts), len(group_b.alerts)) / max(len(group_a.alerts), len(group_b.alerts))))
    return 0.0
  s = 0.0
  alert_matching = find_alert_matching(group_a.alerts, group_b.alerts, early_stopping_threshold=early_stopping_threshold, w=w, min_alert_match_similarity=min_alert_match_similarity)
  used_a = []
  used_b = []
  alignment_a = []
  alignment_b = []
  for a, b in alert_matching:
    if a not in used_a and b not in used_b:
      used_a.append(a)
      used_b.append(b)
      s += alert_matching[(a, b)]
      if alignment_weight != 0.0:
        alignment_a.append(group_a.alerts.index(a))
        alignment_b.append(group_b.alerts.index(b))
  if partial == False:
    s /= max(len(group_a.alerts), len(group_b.alerts)) # Normalize to [0, 1]
    # Unordered alert matches have a decreased similarity
    if alignment_weight != 0.0 and len(alignment_a) > 0 and len(alignment_b) > 0:
      # Only consider alerts with matches, non-matching alerts are already included in similarity when dividing by max length of alerts
      s = s * (1 - alignment_weight) + (editdistance.eval(alignment_a, alignment_b) / max(len(alignment_a), len(alignment_b))) * alignment_weight
  else:
    s /= len(group_a.alerts) # Only care about how well group_a is represented in group_b
  return s

def get_group_similarity_bag(group_a, group_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0, alignment_weight=0.0, partial=False):
  s = 0.0
  # Similarity is based on relative frequency deviations from group_a and group_b respective bag of alerts (bag representatives are aligned)
  if min(len(group_a.bag_of_alerts), len(group_b.bag_of_alerts)) / max(len(group_a.bag_of_alerts), len(group_b.bag_of_alerts)) < early_stopping_threshold:
    return 0.0
  alert_matching = find_alert_matching(group_a.bag_of_alerts.keys(), group_b.bag_of_alerts.keys(), early_stopping_threshold=0.0, w=w, min_alert_match_similarity=min_alert_match_similarity) # Set early stopping to 0.0 for bag since grouping criteria do not match
  used_a = []
  used_b = []
  for a, b in alert_matching:
    if a not in used_a and b not in used_b:
      used_a.append(a)
      used_b.append(b)
      group_a_type = type(group_a.bag_of_alerts[a])
      group_b_type = type(group_b.bag_of_alerts[b])
      if group_a_type is tuple and group_b_type is tuple:
        # Both have intervals, check if there is an overlap
        if min(group_a.bag_of_alerts[a][1], group_b.bag_of_alerts[b][1]) >= max(group_a.bag_of_alerts[a][0], group_b.bag_of_alerts[b][0]):
          s += 1
        elif group_a.bag_of_alerts[a][1] < group_b.bag_of_alerts[b][0]:
          # interval of a is lower than interval of b
          s += group_a.bag_of_alerts[a][1] / group_b.bag_of_alerts[b][0]
        else:
          # interval of a is higher than interval of b
          s += group_b.bag_of_alerts[b][1] / group_a.bag_of_alerts[a][0]
      elif group_a_type is tuple:
        # group_a has interval, check if b is inside
        if group_a.bag_of_alerts[a][0] <= group_b.bag_of_alerts[b] <= group_a.bag_of_alerts[a][1]:
          s += 1
        elif group_a.bag_of_alerts[a][0] > group_b.bag_of_alerts[b]:
          # b is lower than interval of a
          s += group_b.bag_of_alerts[b] / group_a.bag_of_alerts[a][0]
        else:
          # b is higher than interval of a
          s += group_a.bag_of_alerts[a][1] / group_b.bag_of_alerts[b]
      elif group_b_type is tuple:
        # group_a has interval, check if b is inside
        if group_b.bag_of_alerts[b][0] <= group_a.bag_of_alerts[a] <= group_b.bag_of_alerts[b][1]:
          s += 1
        elif group_b.bag_of_alerts[b][0] > group_a.bag_of_alerts[a]:
          # a is lower than interval of b
          s += group_a.bag_of_alerts[a] / group_b.bag_of_alerts[b][0]
        else:
          # a is higher than interval of b
          s += group_b.bag_of_alerts[b][1] / group_a.bag_of_alerts[a]
      else:
        s += min(group_a.bag_of_alerts[a], group_b.bag_of_alerts[b]) / max(group_a.bag_of_alerts[a], group_b.bag_of_alerts[b])
  if partial == False:
    s /= max(len(group_a.bag_of_alerts), len(group_b.bag_of_alerts))
  else:
    s /= len(group_a.bag_of_alerts)
  return s

from cdifflib import CSequenceMatcher
import time

def get_group_similarity_alignment(group_a, group_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0, alignment_weight=0.0, partial=False):
  if min(len(group_a.merge_seq), len(group_b.merge_seq)) / max(len(group_a.merge_seq), len(group_b.merge_seq)) < early_stopping_threshold:
    return 0.0
  s = 0.0
  alert_matching = find_alert_matching(group_a.bag_of_alerts.keys(), group_b.bag_of_alerts.keys(), early_stopping_threshold=0.0, w=w, min_alert_match_similarity=min_alert_match_similarity) # Set early stopping to 0.0 for bag since grouping criteria do not match
  used_a = []
  used_b = []
  b_to_a = {}
  for a, b in alert_matching:
    if a not in used_a and b not in used_b:
      used_a.append(a)
      used_b.append(b)
      b_to_a[b] = a
  alignment_a = []
  alignment_b = []
  for a in group_a.merge_seq:
    if a in used_a:
      alignment_a.append(used_a.index(a))
    else:
      # No match found, use max index + 1
      alignment_a.append(len(used_a))
  for b in group_b.merge_seq:
    if b in b_to_a:
      a_eq = b_to_a[b]
      alignment_b.append(used_a.index(a_eq))
    else:
      # No match found, use max index + 2
      alignment_b.append(len(used_a) + 1)
  if alignment_weight != 0.0 and len(alignment_a) > 0 and len(alignment_b) > 0:
    sm = CSequenceMatcher(None, alignment_a, alignment_b, autojunk=False)
    if partial is False:
      if len(alignment_a) * len(alignment_b) > (10000 * 10000):
          # For very large sequences, only an estimation for the upper bound can be reasonably used due to the high complexity of LCS computation
          return sm.real_quick_ratio() # Either use sm.quick_ratio() or sm.real_quick_ratio()
      else:
          return sum([block.size for block in sm.get_matching_blocks()]) / min(len(alignment_a), len(alignment_b))
    else:
      lcs_len = sum([block.size for block in sm.get_matching_blocks()])
      return lcs_len / len(alignment_a)
  return 0.0

def get_group_similarity(group_a, group_b, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=0.0, alignment_weight=0.0, strategy='best', partial=False):
  # alerts_a, alerts_b are lists of alert objects
  if strategy == 'avg':
    return get_group_similarity_avg(group_a, group_b, early_stopping_threshold, w, min_alert_match_similarity, alignment_weight, partial)
  elif strategy == 'best':
    return get_group_similarity_exact(group_a, group_b, early_stopping_threshold, w, min_alert_match_similarity, alignment_weight, partial)
  elif strategy == 'bag':
    s_bag = 0
    if alignment_weight != 1.0:
      s_bag = get_group_similarity_bag(group_a, group_b, early_stopping_threshold, w, min_alert_match_similarity, alignment_weight, partial)
    s_alignment = 0
    if alignment_weight != 0.0:
      s_alignment = get_group_similarity_alignment(group_a, group_b, early_stopping_threshold, w, min_alert_match_similarity, alignment_weight, partial)
    return s_bag * (1 - alignment_weight) + s_alignment * alignment_weight
  else:
    print('Unknown group similarity strategy!')
