from merging.objects import Wildcard, Mergelist
from preprocessing.objects import Alert
from collections import Counter
from similarity import similarity
import math

def merge_json(alerts, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0):
  keys_list = []
  # Count key occurrences
  for alert in alerts:
    keys_list.extend(alert.keys())
  c_keys = Counter(keys_list)
  # Ignore infrequent keys
  key_types = {}
  for key, freq in c_keys.items():
    if freq / len(alerts) >= min_key_occurrence:
      # Store value types for each key in dict
      key_types[key] = set()
      for alert in alerts:
        if key not in alert:
          # Key not present in this alert; do nothing
          continue
        key_type = type(alert[key])
        if key_type is dict:
          key_types[key].add('dict')
        elif key_type is list:
          key_types[key].add('list')
        else:
          key_types[key].add('value')
  # Generate meta-alert as merge of all alerts
  merge = {}
  for key, key_type in key_types.items():
    values = []
    if key_type == {'dict'}:
      # No need to analyze values in dictionary, just call this method recursively for all values
      for alert in alerts:
        if key not in alert:
          continue
        v = alert[key]
        if type(v) is Mergelist:
          # Value is a Mergelist, extract its elements and treat as list of values
          values.extend(v.elements)
        else:
          # Value is not a Mergelist, treat as normal value
          values.append(v)
      merge[key] = merge_json(values, max_val_limit, min_key_occurrence, min_val_occurrence)
    else:
      # Lists are not hashable, not possible to use dict or Counter
      values_unique = []
      values_freq = []
      set_wildcard = False
      values_select = []
      for alert in alerts:
        if key not in alert:
          continue
        v = alert[key]
        if type(v) is Wildcard:
            # If any value is a wildcard, all values will be merged into a wildcard
            set_wildcard = True
            break
        if type(v) is Mergelist:
          # Value is a Mergelist, extract its elements and treat as list of values
          values.extend(v.elements)
          for mergelist_value in v.elements:
            if mergelist_value not in values_unique:
              values_unique.append(mergelist_value)
              values_freq.append(1)
            else:
              values_freq[values_unique.index(mergelist_value)] += 1
        else:
          # Value is not a Mergelist, treat as normal value
          values.append(v)
          if v not in values_unique:
            values_unique.append(v)
            values_freq.append(1)
          else:
            values_freq[values_unique.index(v)] += 1
        values_select = []
        if max_val_limit is not None and len(values_unique) > max_val_limit:
          for i in range(len(values_unique)):
            if values_freq[i] / len(values) >= min_val_occurrence:
              values_select.append(values_unique[i])
          if len(values_select) == 0 or len(values_select) > max_val_limit:
            # If too many values occur or all values are equally rare, merge them into a wildcard
            set_wildcard = True
            break
      # Set value either as wildcard (if too many distinct values occur) or a mergelist otherwise
      if set_wildcard:
        merge[key] = Wildcard([])
      else:
        values_select = []
        for i in range(len(values_unique)):
          if values_freq[i] / len(values) >= min_val_occurrence:
            values_select.append(values_unique[i])
        merge[key] = Mergelist(values_select)

  return merge

from clustering.objects import Group
import time

def merge_group(groups, min_alert_match_similarity=0.0, max_alerts_for_exact_matching=100, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0):
  merge = Group()
  merged_bag_of_alerts, merged_alerts, merged_bags, merged_bags_inv = merge_bag(groups, min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
  max_alerts = -1
  # Find largest group, because it has the most alerts to be matched to
  group_max_alerts = None
  for group in groups:
    if len(group.alerts) > max_alerts:
      group_max_alerts = group
      max_alerts = len(group.alerts)
    merge.attacks.update(group.attacks) # Labels of merge is union of group labels
  merge.bag_of_alerts = merged_bag_of_alerts
  merge.merge_seq = merge_seq_alignment(groups, merged_bags, merged_bags_inv)
  if max_alerts <= max_alerts_for_exact_matching:
    merge.alerts = merge_exact(groups, min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, group_max_alerts=group_max_alerts)
  else:
    merge.alerts = merged_alerts
  if len(merge.alerts) == 0:
    print('Something went wrong, group with 0 alerts generated:')
    print(merge)

  return merge

def merge_exact(groups, min_alert_match_similarity=0.0, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0, group_max_alerts=None):
  # Compute similarities for each combination of alerts between group and merge
  # Connect the ones with the highest of all, proceed with second highest, etc.
  # Skip the ones that are already taken and proceed with next ones.
  # Add the ones that are left as new alerts in merge.
  # Also take offset in positions into account when computing similarity (timing?), might help with collisions even if just small weight
  if group_max_alerts is None:
    # In case that it was already computed before (e.g., in merge_group), do not compute largest group again
    max_alerts = -1
    # Find largest group, because it has the most alerts to be matched to
    for group in groups:
      if len(group.alerts) > max_alerts:
        group_max_alerts = group
        max_alerts = len(group.alerts)
  alerts_to_merge = {} # dict holding all lists of alerts to be merged
  for alert in group_max_alerts.alerts:
    alerts_to_merge[alert] = [alert]
  for group in groups:
    if group == group_max_alerts:
      # Alerts in this group were already added to alerts_to_merge
      continue
    else:
      alert_matching = similarity.find_alert_matching(group.alerts, alerts_to_merge, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=min_alert_match_similarity)
      used_m = []
      used_g = []
      for alert_g, alert_m in alert_matching:
        if alert_m not in used_m and alert_g not in used_g: # Make sure that each alert_g points to one alert_m
          used_m.append(alert_m)
          used_g.append(alert_g)
          alerts_to_merge[alert_m].append(alert_g)
      # In case that alerts in group were not matched (e.g., all matching similarities < min_alert_match_similarity), add them to merge as single alerts
      missing_alerts = set(group.alerts) - set(used_g)
      for missing_alert in missing_alerts: 
        alerts_to_merge[missing_alert] = [missing_alert]
  merged_alerts = []
  for alerts in alerts_to_merge.values():
    json_alerts = []
    for alert in alerts:
      json_alerts.append(alert.d)
    merged_alert = Alert(merge_json(json_alerts, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence))
    merged_alerts.append(merged_alert)
  return merged_alerts

from cdifflib import CSequenceMatcher
import time

def merge_seq_alignment(groups, merged_bags, merged_bags_inv):
  # For efficiency, alignment is created incrementally. This does not guarantee optimal alignment.
  lcs = []
  merge_list = list(merged_bags.keys())
  first_alignment = True
  for group in groups:
    alignment = []
    for alert in group.merge_seq:
      alignment.append(merge_list.index(merged_bags_inv[alert]))
    if len(alignment) > 10000:
       # Unfortunately, computing LCS for very long alignments does not scale; one of the alignments is used for merge without computing LCS.
       lcs = alignment
       break
    if first_alignment is True:
      lcs = alignment
      first_alignment = False
    else:
      sm = CSequenceMatcher(None, lcs, alignment, autojunk=False) # During testing, autojunk=True sometimes incorrectly returned empty lists
      l = [lcs[block.a:(block.a + block.size)] for block in sm.get_matching_blocks()]
      lcs = [item for sublist in l for item in sublist]
  seq = []
  for alert_index in lcs:
    seq.append(merge_list[alert_index])
  return seq

def merge_bag(groups, min_alert_match_similarity=0.0, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0):
  max_alert_patterns = -1
  group_max_alert_patterns = None
  # Find largest group, because it has the most alert patterns to be matched to
  for group in groups:
    if len(group.bag_of_alerts) > max_alert_patterns:
      group_max_alert_patterns = group
      max_alert_patterns = len(group.bag_of_alerts)
  alert_patterns_to_merge = {}
  for alert_pattern, freq in group_max_alert_patterns.bag_of_alerts.items():
    alert_patterns_to_merge[alert_pattern] = [(alert_pattern, freq)]
  for group in groups:
    if group == group_max_alert_patterns:
      # Alert patterns in this group were already added to alert_patterns_to_merge
      continue
    else:
      alert_matching = similarity.find_alert_matching(group.bag_of_alerts, alert_patterns_to_merge, early_stopping_threshold=0.0, w=None, min_alert_match_similarity=min_alert_match_similarity) # Early stopping threshold should not be used for bag matching, since it does not correspond to grouping criteria
      used_m = []
      used_g = []
      for alert_g, alert_m in alert_matching:
        if alert_m not in used_m and alert_g not in used_g: # Make sure that each alert_g points to one alert_m
          used_m.append(alert_m)
          used_g.append(alert_g)
          alert_patterns_to_merge[alert_m].append((alert_g, group.bag_of_alerts[alert_g]))
      # In case that alerts in group were not matched (e.g., all matching similarities < min_alert_match_similarity), add them to merge as single alerts
      missing_alerts = set(group.bag_of_alerts) - set(used_g)
      for missing_alert in missing_alerts:
        alert_patterns_to_merge[missing_alert] = [(missing_alert, group.bag_of_alerts[missing_alert])]
  merged_bag_of_alerts = {}
  merged_alerts = []
  merged_bags = {}
  merged_bags_inv = {}
  for alert_pattern, alert_tuples in alert_patterns_to_merge.items():
    json_alerts = []
    frequencies = []
    raw_alerts = []
    for alert_pattern, freq in alert_tuples:
      json_alerts.append(alert_pattern.d)
      frequencies.append(freq)
      raw_alerts.append(alert_pattern)
    json_merge = Alert(merge_json(json_alerts, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence))
    first_frequency = frequencies[0] # Start values for min max search
    max_frequency = -1
    if type(first_frequency) is int:
      min_frequency = first_frequency
    elif type(first_frequency) is tuple:
      min_frequency = first_frequency[0]
    for frequency in frequencies:
      if type(frequency) is int:
        min_frequency = min(min_frequency, frequency)
        max_frequency = max(max_frequency, frequency)
      elif type(frequency) is tuple:
        min_frequency = min(min_frequency, frequency[0], frequency[1])
        max_frequency = max(max_frequency, frequency[0], frequency[1])
    if min_frequency == max_frequency:
      merged_bag_of_alerts[json_merge] = min_frequency
    else:
      merged_bag_of_alerts[json_merge] = (min_frequency, max_frequency)
    # In case that this group will be used for comparison, add unordered list of alerts according to respective frequencies
    for i in range(math.ceil((max_frequency + min_frequency) / 2)):
      merged_alerts.append(json_merge)
    merged_bags[json_merge] = raw_alerts
    for raw_alert in raw_alerts:
      merged_bags_inv[raw_alert] = json_merge
  return merged_bag_of_alerts, merged_alerts, merged_bags, merged_bags_inv
