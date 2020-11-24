import re
from collections import deque
import json

class Wildcard:
  def __init__(self, elements=None):
    self.elements = []
    if elements is not None:
      self.elements.extend(elements)
    self.symbol = '§'

  def __repr__(self):
    return self.symbol

class Mergelist:
  def __init__(self, elements):
    self.elements = []
    if elements is not None:
      self.elements.extend(elements)
    self.symbol = '[]'

  def add(self, element):
    if element not in self.elements:
      self.elements.append(element)

  def toWildcard(self):
    return Wildcard(self.elements)

  def __repr__(self):
    res = self.symbol[0]
    for element in self.elements:
      res += json.dumps(element) + ', '
    return res[:-2] + self.symbol[-1]

import random

def get_log_int(max_bits):
  """Get a log-distributed random integer integer in range 0 to maxBits-1."""
  rand_bits = random.randint(0, (1 << max_bits) - 1)
  result = 0
  while (rand_bits & 1) != 0:
    result += 1
    rand_bits >>= 1
  return result

from similarity import similarity
from merging import merge
import time

class MetaAlert:
  def __init__(self, mam):
    self.mam = mam
    self.alert_group = None
    self.support = {}

  def update_alert(self, match_similarity, min_alert_match_similarity=0.0, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0):
    if match_similarity != 1.0:
      # To improve performance, ignore that it is possible that merge changes even if perfect match is added, e.g., when some key reaches min_key_occurrence
      self.alert_group = merge.merge_group(self.mam.kb.get_groups(self), min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
    self.support = {}
    for group in self.mam.kb.get_groups(self):
      for f in group.files:
        if f not in self.support:
          self.support[f] = 1
        else:
          self.support[f] += 1

  def get_json_representation(self, limit=10, offset=''):
    return self.alert_group.get_json_representation(limit, offset)

  def __repr__(self):
    res = 'Meta-Alert with ' + str(len(self.mam.kb.get_groups(self))) + ' allocated groups: ' + str(self.support) + '\n' + str(self.alert_group)
    i = 1
    for group in self.mam.kb.get_groups(self):
      res += '\n ' + 'Group #' + str(i) + ': ' + str(group)
      i += 1
    return res

class MetaAlertManager:
  def __init__(self, kb):
    self.kb = kb
    self.meta_alerts = {}

  def add_to_meta_alerts(self, group, delta, threshold, min_alert_match_similarity=0.0, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0, bag_limit=2000, w=None, alignment_weight=0.0, force_label=None, partial=False):
    # Side-effect of this method is to set group.meta_alert
    if len(group.bag_of_alerts) == 0:
      group.create_bag_of_alerts(min_alert_match_similarity, max_val_limit, min_key_occurrence, min_val_occurrence)
    best_matching_meta_alert, maxSimilarity = self.get_most_similar_meta_alert(group=group, delta=delta, threshold=threshold, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, bag_limit=bag_limit, w=w, alignment_weight=alignment_weight, force_label=force_label, partial=partial)
    if maxSimilarity >= threshold:
      self.kb.add_group_meta_alert(group, best_matching_meta_alert)
      best_matching_meta_alert.update_alert(maxSimilarity, min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
      return False # Indicates that no new meta-alert was generated
    else:
      meta_alert = MetaAlert(self)
      self.kb.add_group_meta_alert(group, meta_alert)
      meta_alert.update_alert(maxSimilarity, min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
      if delta in self.meta_alerts:
        self.meta_alerts[delta].append(meta_alert)
      else:
        self.meta_alerts[delta] = [meta_alert]
      return True # Indicates that a new meta-alert was generated

  def get_most_similar_meta_alert(self, group, delta, threshold, min_alert_match_similarity=0.0, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0, bag_limit=2000, w=None, alignment_weight=0.0, force_label=None, partial=False):
    if len(group.bag_of_alerts) == 0:
      group.create_bag_of_alerts(min_alert_match_similarity, max_val_limit, min_key_occurrence, min_val_occurrence)
    maxSimilarity = -1.0
    best_matching_meta_alert = None
    s = None
    if delta in self.meta_alerts:
      for meta_alert in self.meta_alerts[delta]:
        if len(group.alerts) * len(meta_alert.alert_group.alerts) > bag_limit:
          s = similarity.get_group_similarity(group, meta_alert.alert_group, early_stopping_threshold=threshold, w=w, min_alert_match_similarity=min_alert_match_similarity, alignment_weight=alignment_weight, strategy='bag', partial=partial)
        else:
          s = similarity.get_group_similarity(group, meta_alert.alert_group, early_stopping_threshold=threshold, w=w, min_alert_match_similarity=min_alert_match_similarity, alignment_weight=alignment_weight, strategy='best', partial=partial)
        if s > maxSimilarity and (force_label is None or meta_alert.alert_group.attacks == force_label): # If force label is True, only allow meta_alerts with that group label
          maxSimilarity = s
          best_matching_meta_alert = meta_alert
          if s == 1.0:
            # Meta_alert with perfect similarity found, do not check all other meta_alerts
            break
    return best_matching_meta_alert, maxSimilarity  

  def get_json_representation(self, limit=10):
    res = '[\n'
    for delta, meta_alerts in self.meta_alerts.items():
      for meta_alert in meta_alerts:
        res += '{\n\t"delta": "' + str(delta) + '",\n'
        #res += '\t"groups": "' + str(self.kb.meta_alert_dict_unlimited[meta_alert]) + '",\n' # Debug output
        res += '\t"meta_alert_group": ' + meta_alert.get_json_representation(limit, '\t')
        res += '\n},\n'
    return res[:-2] + '\n]'
  
  def __repr__(self):
    res = 'Meta-Alert-Manager with ' + str(sum([len(groups) for delta, groups in self.meta_alerts.items()])) + ' meta-alerts:'
    i = 1
    for delta, meta_alerts in self.meta_alerts.items():
      for meta_alert in meta_alerts:
        res += '\n' + 'Meta-Alert #' + str(i) + '\n' + str(meta_alert)
        i += 1
    return res

class KnowledgeBase:
  def __init__(self, limit=None, queue_strategy='logarithmic', evaluate=False):
      self.delta_dict = {}
      self.meta_alert_dict = {}
      self.limit = limit
      self.queue_strategy = queue_strategy # 'logarithmic' or 'linear', ignored when limit is None
      self.evaluate = evaluate # Flag for evaluation that requires storing additional data
      self.meta_alert_dict_unlimited = {} # For evaluation

  def add_group_delta(self, group, delta):
    if delta in self.delta_dict:
      # Uncomment following lines to only store at most self.limit elements per delta in kb. Note that this can lead to missing groups in evaluation.
      #if self.limit is not None and len(self.delta_dict[delta]) > self.limit:
      #  self.delta_dict[delta].popleft()
      self.delta_dict[delta].append(group)
    else:
      self.delta_dict[delta] = deque([group])

  def add_group_meta_alert(self, group, meta_alert):
    if self.evaluate is True:
      # Following lines are for evaluation and can be ignored for normal operation.
      if meta_alert in self.meta_alert_dict_unlimited:
        self.meta_alert_dict_unlimited[meta_alert].append(group)
      else:
        self.meta_alert_dict_unlimited[meta_alert] = [group]
    group.meta_alert = meta_alert
    if self.limit is None:
      # If queues can grow infinitely, just add each group to the queue
      if meta_alert in self.meta_alert_dict:
        self.meta_alert_dict[meta_alert].append(group)
      else:
        self.meta_alert_dict[meta_alert] = [group]
    elif self.queue_strategy == 'linear':
      # Remove last group for each newly added group after surpassing limit
      if meta_alert in self.meta_alert_dict:
        if len(self.meta_alert_dict[meta_alert]) >= self.limit:
          self.meta_alert_dict[meta_alert].popleft()
        self.meta_alert_dict[meta_alert].append(group)
      else:
        self.meta_alert_dict[meta_alert] = deque([group])
    elif self.queue_strategy == 'logarithmic':
      # As long as the queue is not full, just insert each group normally
      # When the queue is full, replace last element with group with 50% chance, move last element one step back and insert group at the end with 25% chance, move last two elements with 12.5% chance, etc.
      if meta_alert in self.meta_alert_dict:
        if len(self.meta_alert_dict[meta_alert]) < self.limit:
          self.meta_alert_dict[meta_alert].append(group)
        else:
          move_pos = get_log_int(self.limit - 1)
          self.meta_alert_dict[meta_alert] = self.meta_alert_dict[meta_alert][:self.limit - move_pos - 1] + self.meta_alert_dict[meta_alert][self.limit - move_pos:] + [group]
      else:
        self.meta_alert_dict[meta_alert] = [group]

  def get_groups(self, meta_alert):
    return self.meta_alert_dict[meta_alert]

  def hierarchical_clustering(self, labels, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0, early_stopping_threshold=0.0, w=None, alignment_weight=0.0, min_alert_match_similarity=0.0, bag_limit=2000):
    # This method returns R code for plotting a distance dendrogram (computations are done with similarity instead of distances!)
    sim_matrix = {}
    ret_str = ''
    for delta, groups in self.delta_dict.items():
      # Start the recursion
      ret_str += self.hierarchical_clustering_rec(groups, sim_matrix, {}, labels, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, early_stopping_threshold=early_stopping_threshold, w=w, alignment_weight=alignment_weight, min_alert_match_similarity=min_alert_match_similarity, bag_limit=bag_limit)
      ret_str += '\ntree <- as.dendrogram(source, heightAttribute = "myPlotHeight", hang=0)\nplot(tree, center = TRUE, ylab="Similarity", axes=F)\naxis(side=2, at=seq(0, 1, length=6), labels=seq(1,0,-0.2))\n\n'
    return ret_str

  def hierarchical_clustering_rec(self, groups, sim_matrix, merge_similarities, labels, max_val_limit=None, min_key_occurrence=0.0, min_val_occurrence=0.0, early_stopping_threshold=0.0, w=None, alignment_weight=0.0, min_alert_match_similarity=0.0, bag_limit=2000):
    # This is the recursion method for computing the distance dencrogram.
    # groups will be reduced in each recursion step by 1, since 2 groups are always merged to 1.
    # sim_matrix holds all similarities of the previous step, most of the similarities can be reduced since only 3 groups change (2 are removed, 1 is added)
    # merge_similarities holds the similatities of all groups that are merged in the group reduction step, necessary to store similarities of child nodes and make sure that similarities do not increase after merging.
    # labels are the node names of each group
    merge_groups = []
    max_similarity = -1
    # Compute similarity matrix and identify two most similar groups (store in merge_groups)
    for group_a in groups:
      if group_a not in sim_matrix:
        sim_matrix[group_a] = {}
      for group_b in groups:
        if group_a == group_b:
          # Group always has perfect similarity with itself
          sim_matrix[group_a][group_b] = 1.0
          continue
        s = -1
        if group_b in sim_matrix[group_a]:
          # Reuse similarity score for already computed groups
          s = sim_matrix[group_a][group_b]
        else:
          # Compute similarity score for unseen group pair
          if len(group_a.alerts) * len(group_b.alerts) > bag_limit:
            s = similarity.get_group_similarity(group_a, group_b, early_stopping_threshold=early_stopping_threshold, w=w, min_alert_match_similarity=min_alert_match_similarity, alignment_weight=alignment_weight, strategy='bag')
          else:
            s = similarity.get_group_similarity(group_a, group_b, early_stopping_threshold=early_stopping_threshold, w=w, min_alert_match_similarity=min_alert_match_similarity, alignment_weight=alignment_weight, strategy='best')
          sim_matrix[group_a][group_b] = s
        if s > max_similarity:
          max_similarity = s
          merge_groups = [group_a, group_b]
    # Debug output: Print similarity matrix in each recursion
    #sim_str = ''
    #for group_a, sim_groups in sim_matrix.items():
    #  sim_str += labels[group_a] + ': '
    #  for group_b, sim in sim_groups.items():
    #    sim_str += str(sim) + ', '
    #  sim_str += '\n'
    #print(sim_str)
    # Create merged group from two most similar groups
    merged_group = merge.merge_group(merge_groups, min_alert_match_similarity=min_alert_match_similarity, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence)
    groups.append(merged_group)
    lab = ''
    min_children_similarity = 1.1
    for merge_group in merge_groups:
      # Generate name of merged node
      lab += labels[merge_group] + '+'
      # Remove groups from list of groups considered for further computations
      groups.remove(merge_group)
      if merge_group in merge_similarities:
        # Compute smallest similarity of each merged group as a limit to avoid that dendrogram goes backward due to increased similarity, e.g., due to wildcard insertion
        min_children_similarity = min(min_children_similarity, merge_similarities[merge_group])
      # Delete groups from similarity matrix
      del sim_matrix[merge_group]
      for group_a, sim_groups in sim_matrix.items():
        del sim_groups[merge_group]
    labels[merged_group] = lab[:-1]
    # Avoid that dendrogram goes backward by setting similarity of merged group to minimum of computed similarity and minimum children similarity scores
    merge_similarities[merged_group] = min(max_similarity, min_children_similarity)
    print('Merge ' + lab[:-1] + ' with distance ' + str(1 - merge_similarities[merged_group]) + ' (' + str(1 - max_similarity) + ')\n')
    # Recursion stop criteria
    if len(groups) > 1:
      code = self.hierarchical_clustering_rec(groups, sim_matrix, merge_similarities, labels, max_val_limit=max_val_limit, min_key_occurrence=min_key_occurrence, min_val_occurrence=min_val_occurrence, early_stopping_threshold=early_stopping_threshold, w=w, min_alert_match_similarity=min_alert_match_similarity, bag_limit=bag_limit)
    else:
      # Create dendrogram root node
      code = 'node' + labels[merged_group].replace('+', '').replace('-', '') + ' <- Node$new("' + re.sub('[0-9]', '', labels[merged_group]) + '", myPlotHeight=' + str(1 - merge_similarities[merged_group]) + ')\n'
      code += 'source <- node' + labels[merged_group].replace('+', '').replace('-', '') + '\n'
    for merge_group in merge_groups:
      merge_sim = 1.0
      if merge_group in merge_similarities:
        merge_sim = merge_similarities[merge_group]
      # Add child node for each merged group
      code += 'node' + labels[merge_group].replace('+', '').replace('-', '') + ' <- node' + labels[merged_group].replace('+', '').replace('-', '') + '$AddChild("' + re.sub('[0-9]', '', labels[merge_group]) + '", myPlotHeight=' + str(1 - merge_sim) + ')\n'
    return code
