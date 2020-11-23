import datetime
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
      # Hour starts at 0 and is time zone dependent
      if datetime.datetime(2020, 3, 4, 20, 17, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 18, 00).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 20, 18, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 19, 00).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 20, 21, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 22, 00).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 20, 25, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 31, 00).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 20, 32, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 33, 00).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 20, 35, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 40, 00).timestamp():
        attack.add('exploit')
    elif 'spiral' in logfile:
      if datetime.datetime(2020, 3, 4, 18, 57, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 18, 58, 00).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 19, 1, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 17, 00).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 19, 19, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 20, 00).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 19, 23, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 28, 00).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 19, 28, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 30, 00).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 19, 33, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 38, 00).timestamp():
        attack.add('exploit')
    elif 'insect' in logfile:
      if datetime.datetime(2020, 3, 4, 14, 51, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 14, 52, 00).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 14, 54, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 15, 11, 00).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 15, 11, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 15, 12, 00).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 15, 14, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 15, 17, 00).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 15, 18, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 15, 20, 00).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 15, 24, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 15, 29, 00).timestamp():
        attack.add('exploit')
    elif 'onion' in logfile:
      if datetime.datetime(2020, 3, 4, 19, 43, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 44, 00).timestamp():
        attack.add('nmap')
      elif datetime.datetime(2020, 3, 4, 19, 46, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 47, 00).timestamp():
        attack.add('nikto')
      elif datetime.datetime(2020, 3, 4, 19, 49, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 50, 00).timestamp():
        attack.add('vrfy')
      elif datetime.datetime(2020, 3, 4, 19, 50, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 52, 00).timestamp():
        attack.add('hydra')
      elif datetime.datetime(2020, 3, 4, 19, 55, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 19, 56, 00).timestamp():
        attack.add('upload')
      elif datetime.datetime(2020, 3, 4, 20, 00, 00).timestamp() < ts < datetime.datetime(2020, 3, 4, 20, 5, 00).timestamp():
        attack.add('exploit')
  if len(attack) == 0:
    attack = set(['non-attack'])
  if only_noise_alerts is True:
    attack = set(['noise'])
  group.attacks = set(attack) 
  return logfile.split('_')[1].split('.')[0] + '-' + attack.pop()
