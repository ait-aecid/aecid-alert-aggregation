import similarity
import merging
from preprocessing.objects import Alert
import itertools

class Group:
  # This class defines a group of alerts.
  id_iter = itertools.count()

  def __init__(self):
    self.id = next(Group.id_iter)
    self.alerts = []
    self.meta_alert = None
    self.subgroups = []
    self.supergroups = []
    self.bag_of_alerts = {}
    self.merge_seq = []
    self.files = []
    self.attacks = set() # Labels, e.g., name of attack phase

  def add_to_group(self, alerts):
    # Adds one or more alerts to this group.
    if isinstance(alerts, list):
      for alert in alerts:
        self.alerts.append(alert)
        alert.groups_id.append(self.id)
        if alert.file not in self.files:
          self.files.append(alert.file)
    else:
      self.alerts.append(alerts)
      alerts.groups_id.append(self.id)
      if alerts.file not in self.files:
        self.files.append(alerts.file)

  def create_bag_of_alerts(self, threshold, max_val_limit, min_key_occurrence, min_val_occurrence):
    # Computes a bag-of-alerts model for this group.
    self.bag_of_alerts = {} # Remove current bag_of_alerts, create new one from current alerts
    self.merge_seq = [] # Remove current merge_seq, create new one from current alerts
    alerts_to_merge = {}
    alerts_template_dict = {}
    for alert in self.alerts:
      max_s = -1
      best_matching_alert_template = None
      for alert_template in alerts_to_merge:
        s = similarity.similarity.get_json_similarity(alert.d, alert_template.d)
        if s >= max_s:
          max_s = s
          best_matching_alert_template = alert_template
      if max_s >= threshold:
        alerts_to_merge[best_matching_alert_template].append(alert.d)
        alerts_template_dict[alert] = best_matching_alert_template
      else:
        alerts_to_merge[alert] = [alert.d]
        alerts_template_dict[alert] = alert
    template_merge_dict = {}
    for template, alerts_to_merge_list in alerts_to_merge.items():
      merge = Alert(merging.merge.merge_json(alerts_to_merge_list, max_val_limit, min_key_occurrence, min_val_occurrence))
      self.bag_of_alerts[merge] = len(alerts_to_merge_list)
      template_merge_dict[template] = merge
    for alert in self.alerts:
      self.merge_seq.append(template_merge_dict[alerts_template_dict[alert]])

  def get_json_representation(self, limit=10, offset=''):
    res = '\n' + offset + '['
    #res += '\n' + offset + '"label": ' + str(self.attacks) + '\n' # Debugging info
    if (len(self.alerts) == 0 and len(self.bag_of_alerts) != 0) or len(self.alerts) > limit:
      for alert_pattern, freq in self.bag_of_alerts.items():
        res += '\n' + offset + '{\n'
        if isinstance(freq, tuple):
          res += offset + '\t' + '"min_frequency": ' + str(freq[0]) + ',\n'
          res += offset + '\t' + '"max_frequency": ' + str(freq[1]) + ',\n'
        else:
          res += offset + '\t' + '"min_frequency": ' + str(freq) + ',\n'
          res += offset + '\t' + '"max_frequency": ' + str(freq) + ',\n'
        res += offset + '\t' + '"meta_alert": \n' + str(alert_pattern.get_json_representation(offset + '\t'))
        res += '\n' + offset + '},'
    else:
      for alert in self.alerts:
        res += '\n' + offset + '{\n'
        res += offset + '\t' + '"min_frequency": 1,\n'
        res += offset + '\t' + '"max_frequency": 1,\n'
        res += offset + '\t' + '"meta_alert": \n' + str(alert.get_json_representation(offset + '\t'))
        res += '\n' + offset + '},'
    return res[:-1] + '\n' + offset + ']'

  def __repr__(self):
    res = ' Group ' + str(self.id) + ' with ' + str(len(self.alerts)) + ' alerts'
    # Also provide information on input file, comment out if no needed.
    if len(self.files) > 0 and self.files[0] is not None:
      res += ' ('
      for f in self.files:
        res += f + ', '
      res = res[:-2] + ')'
    if len(self.supergroups) > 0:
      res += ', supergroups=['
      for supergroup in self.supergroups:
        res += str(supergroup.id) + ', '
      res = res[:-2] + ']'
    if len(self.subgroups) > 0:
      res += ', subgroups=['
      for subgroup in self.subgroups:
        res += str(subgroup.id) + ', '
      res = res[:-2] + ']'
    if len(self.attacks) > 0:
      res += ', labels=['
      for attack in list(self.attacks):
        res += str(attack)
      res = res[:-2] + ']'
    # In case that only bag_of_alerts is set or when number of alerts exceeds certain limit, output bag information
    if (len(self.alerts) == 0 and len(self.bag_of_alerts) != 0) or len(self.alerts) > 10:
      for alert_pattern, freq in self.bag_of_alerts.items():
        res += '\n  ' + str(freq) + ' x ' + str(alert_pattern)
    else:
      i = 1
      for alert in self.alerts:
        res += '\n  ' + 'Alert #' + str(i) + ' ' + str(alert)
        i += 1
    return res
