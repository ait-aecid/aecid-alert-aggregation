from preprocessing import preprocess
from clustering import time_delta_group
import random

def read_input(files, deltas, input_type, noise=0.0):
  groups_dict = {}
  for filegroup in files:
    alerts = []
    timestamps = []
    for f in filegroup:
      f_parts = f.split('/')
      file_type = None
      if len(f_parts) > 1:
        file_type = f_parts[1]
      if input_type == 'aminer' or file_type == 'aminer':
        file_alerts, file_timestamps = preprocess.read_aminer_json(f)
      elif input_type == 'ossec' or file_type == 'ossec':
        file_alerts, file_timestamps = preprocess.read_ossec_full_json(f)
      else:
        print('Unknown file type. Please specify input_type. Aborting.')
        break
      if len(file_alerts) != len(file_timestamps):
        print('Alerts and timestamps are diverging, something went wrong during input file preprocessing!')
        break
      alerts.extend(file_alerts)
      timestamps.extend(file_timestamps)

    if noise != 0.0:
      # Noise specifies the average amount of injected false alarms per minute, measured from first to last occurring alert
      max_ts = max(timestamps)
      min_ts = min(timestamps)
      number_to_inject = (max_ts - min_ts) / 60.0 * noise
      sample_alerts = random.sample(alerts, min(100, len(alerts)))
      while number_to_inject > 0:
        number_to_inject -= 1
        new_alert = random.choice(sample_alerts).get_alert_clone()
        new_alert.noise = True
        alerts.append(new_alert)
        timestamps.append(random.uniform(min_ts, max_ts))

    deltas.sort() # deltas have to be sorted for correct group subgroups and supergroup!
    prev_groups = None
    delta_dict = {}
    for delta in deltas:
      group_times = time_delta_group.get_time_delta_group_times(timestamps, delta)
      groups = time_delta_group.get_groups(alerts, timestamps, group_times)
      if prev_groups is None:
        prev_groups = groups # Initial pass, i.e., groups with smallest delta
      else:
        time_delta_group.find_group_connections(prev_groups, groups)
        prev_groups = groups # Use group in next iteration when delta is one step larger
      print('delta = ' + str(delta) + ': ' + str(len(groups)) + ' groups in ' + str(filegroup))
      # Debugging output: Print each group interval with number of alerts per group
      #for group_time in group_times:
      #  print(str(group_time) + ': ' + str(len(groups[group_times.index(group_time)].alerts)))
      delta_dict[delta] = groups
    groups_dict[files.index(filegroup)] = delta_dict
  return groups_dict
