import datetime
from datetime import timezone
from dateutil import parser

def label_group(group):
  logfile = group.files[0]
  attack = set()
  only_noise_alerts = True
  for alert in group.alerts:
    ts = 0
    if 'timestamp' in alert.d:
      ts = parser.parse(alert.d['timestamp']).timestamp()
    elif 'LogData' in alert.d and 'Timestamps' in alert.d['LogData']:
      ts = alert.d['LogData']['Timestamps'][0]
    else:
      print('Unknown alert ' + str(alert))
    if alert.noise is False:
      only_noise_alerts = False
    if 'cup' in logfile:
      if datetime.datetime(2020, 3, 4, 19, 17, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 18, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 19, 18, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 19, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 19, 21, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 22, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 19, 25, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 31, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 19, 32, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 33, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 19, 35, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 40, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('exploit')
    elif 'spiral' in logfile:
      if datetime.datetime(2020, 3, 4, 17, 57, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 17, 58, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 18, 1, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 17, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 18, 19, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 20, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 18, 23, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 28, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 18, 28, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 30, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 18, 33, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 38, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('exploit')
    elif 'insect' in logfile:
      if datetime.datetime(2020, 3, 4, 13, 51, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 13, 52, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 13, 54, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 11, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 14, 11, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 12, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 14, 14, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 17, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 14, 18, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 20, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 14, 24, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 29, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('exploit')
    elif 'onion' in logfile:
      if datetime.datetime(2020, 3, 4, 18, 43, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 44, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 18, 46, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 47, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 18, 49, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 50, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 18, 50, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 52, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 18, 55, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 56, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 19, 00, 00).replace(tzinfo=timezone.utc).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 5, 00).replace(tzinfo=timezone.utc).timestamp():
        attack.add('exploit')
  if len(attack) == 0:
    attack = set(['non-attack'])
  if only_noise_alerts is True:
    attack = set(['noise'])
  group.attacks = set(attack) 
  return logfile.split('_')[1].split('.')[0] + '-' + attack.pop()
