import datetime
from datetime import timezone
from dateutil import parser
from attacktimes import get_phase
from datetime import datetime

def label_group(group):
  logfile_parts = group.files[0].split('/')[-1].split('.')[0].split('_')
  # Alert files are sometimes named fox_aminer or aminer_cup; i.e., relevant scenario name is either first or second and needs to be extracted
  if logfile_parts[0] == "aminer" or logfile_parts[0] == "wazuh" or logfile_parts[0] == "ossec" or logfile_parts[0] == "test":
    logfile = logfile_parts[1]
  else:
    logfile = logfile_parts[0]
  attack = set()
  only_noise_alerts = True
  for alert in group.alerts:
    ts = 0
    if 'timestamp' in alert.d:
      # For Wazuh alerts from the AIT-LDSv1.1
      ts = parser.parse(alert.d['timestamp']).timestamp()
    elif '@timestamp' in alert.d:
      # For Wazuh alerts from the AIT-ADS
      ts = datetime.strptime(alert.d['@timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
    elif 'LogData' in alert.d and 'Timestamps' in alert.d['LogData']:
      # For AMiner alerts
      ts = alert.d['LogData']['Timestamps'][0]
    else:
      print('Unknown alert ' + str(alert))
    if alert.noise is False:
      only_noise_alerts = False
    attack_label = get_phase(logfile, ts)
    if attack_label != "":
        attack.add(attack_label)
  if len(attack) == 0:
    attack = set(['non-attack'])
  if only_noise_alerts is True:
    attack = set(['noise'])
  group.attacks = set(attack) 
  return logfile + '-' + attack.pop()
