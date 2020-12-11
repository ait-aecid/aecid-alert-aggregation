from clustering.objects import Group

def get_time_delta_group_times(timestamps, delta):
  # Cannot assume that alerts are chronologically ordered, especially when multiple files/ids are used.
  # This code is not implemented for online analysis, only forensic analysis supported.
  group_times = []
  for ts in timestamps:
    group_found = False
    for i in reversed(range(len(group_times))): # Reverse, because most likely last group is most recent and thus fits
      if ts >= group_times[i][0] - delta and ts <= group_times[i][1] + delta:
        group_times[i] = (min(group_times[i][0], ts), max(group_times[i][1], ts))
        group_found = True
        break
    if group_found is False:
      group_times.append((ts, ts))

  # Sort groups by start time
  start_times = []
  for group_time in group_times:
    start_times.append(group_time[0])
  sorted_group_times = [x for _, x in sorted(zip(start_times, group_times))]

  merged_group_times = [sorted_group_times[0]] # Initialize with first group
  for group_time in sorted_group_times:
    if group_time[0] <= merged_group_times[-1][1] + delta:
      merged_group_times[-1] = (merged_group_times[-1][0], max(merged_group_times[-1][1], group_time[1]))
    else:
      merged_group_times.append(group_time)

  return merged_group_times

def get_group_indices(timestamps, group_times):
  group_indices = []
  for group_time in group_times:
    group_indices.append([])
  i = 0
  for ts in timestamps:
    j = 0
    for group_time in group_times:
      # Alert could be part of multiple groups
      if ts >= group_time[0] and ts <= group_time[1]:
        group_indices[j].append(i)
      j += 1
    i += 1

  return group_indices

def get_groups(alerts, timestamps, group_times):
  groups = []
  for group_time in group_times:
    groups.append(Group())
  i = 0
  for alert in alerts:
    ts = timestamps[i]
    j = 0
    for group_time in group_times:
      # Alert could be part of multiple groups
      if ts >= group_time[0] and ts <= group_time[1]:
        groups[j].add_to_group(alert)
      j += 1
    i += 1

  return groups

def find_group_connections(groups_small_delta, groups_large_delta):
  # This could be improved by finding common group ids allocated to each alert
  # This could be more efficiently solved when group_times is used instead of iterating over all alerts.
  for group_small_delta in groups_small_delta:
    supergroup = None
    for alert in group_small_delta.alerts:
      if supergroup is not None and alert in supergroup.alerts:
        # Alert is in same supergroup as previous alert, skip since supergroup already added.
        continue
      for group_large_delta in groups_large_delta:
        if alert in group_large_delta.alerts:
          supergroup = group_large_delta
          break
      if supergroup is not None:
        group_small_delta.supergroups.append(supergroup)
        if group_small_delta not in supergroup.subgroups:
          supergroup.subgroups.append(group_small_delta)
      else:
        print('No supergroup found, something went wrong!')
