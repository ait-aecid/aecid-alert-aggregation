import json
from dateutil import parser
import re
from preprocessing.objects import Alert
from json import JSONDecodeError
from datetime import datetime

delimiters = '"|,|:| '

def get_src_ip(event):
  ip = ''
  if 'src_ip' in event:
    part = event[event.index('src_ip')+9:]
    ip = re.split(delimiters, part)[0]
  elif 'lip' in event:
    part = event[event.index('lip')+4:]
    ip = re.split(delimiters, part)[0]
  
  return ip

def get_dst_ip(event):
  ip = ''
  if 'dest_ip' in event:
    part = event[event.index('dest_ip')+10:]
    ip = re.split(delimiters, part)[0]
  elif 'rip' in event:
    part = event[event.index('rip')+4:]
    ip = re.split(delimiters, part)[0]

  return ip

def get_src_port(event, src_ip):
  port = -1
  if 'src_port' in event:
    part = event[event.index('src_port')+10:]
    port = re.split(delimiters, part)[0]
  elif len(src_ip) > 0 and src_ip + ':' in event:
    part = event[event.index(src_ip + ':')+len(src_ip)+1:]
    port = re.split(delimiters, part)[0]
  
  return int(port)

def get_dst_port(event, dst_ip):
  port = -1
  if 'dest_port' in event:
    part = event[event.index('dest_port')+11:]
    port = re.split(delimiters, part)[0]
  elif len(dst_ip) > 0 and dst_ip + ':' in event:
    part = event[event.index(dst_ip + ':')+len(dst_ip)+1:]
    port = re.split(delimiters, part)[0]

  return int(port)

def read_ossec_minimal_json(filename):
  alerts = []
  timestamps = []
  with open(filename) as f:
    for line in f:
      entry = json.loads(line)
      alert = {}
      alert['timestamp'] = parser.parse(entry['timestamp']).timestamp()
      if 'data' in entry and 'srcip' in entry['data']:
        alert['srcip'] = re.split(delimiters, entry['data']['srcip'])[0]
      else:
        alert['srcip'] = get_src_ip(entry['full_log'])
      if 'data' in entry and 'dstip' in entry['data']:
        alert['dstip'] = re.split(delimiters, entry['data']['dstip'])[0]
      else:
        alert['dstip'] = get_dst_ip(entry['full_log'])
      alert['srcport'] = get_src_port(entry['full_log'], alert['srcip'])
      alert['dstport'] = get_dst_port(entry['full_log'], alert['dstip'])
      if 'data' in entry and 'proto' in entry['data']:
        alert['proto'] = entry['data']['proto']
      else:
        alert['proto'] = ''
      if 'description' in entry['rule']:
        alert['class'] = entry['rule']['description']
      else:
        alert['class'] = ''
      alert_obj = Alert(alert)
      alert_obj.file = filename
      alerts.append(alert_obj)
      timestamps.append(alert['timestamp'])
  return alerts, timestamps

def read_ossec_full_json(filename):
  alerts = []
  timestamps = []
  with open(filename) as f:
    for line in f:
      if len(line.strip('\n\r')) == 0:
        continue
      json_alert = json.loads(line)
      alert_obj = Alert(json_alert)
      alert_obj.file = filename
      alerts.append(alert_obj)
      if 'timestamp' in alert_obj.d:
          # In alerts from AIT-LDSv1, field is named 'timestamp'
          timestamps.append(parser.parse(alert_obj.d['timestamp']).timestamp())
      else:
          # In alerts from AIT-ADS, field is named '@timestamp'
          timestamps.append(parser.isoparse(alert_obj.d['@timestamp']).timestamp())
  return alerts, timestamps

def read_aminer_json(filename):
  alerts = []
  timestamps = []
  retry_lines = False
  json_alerts = []
  with open(filename) as f:
    try:
      # Try to read entire file as list of alerts (e.g., alerts from the AIT-LDSv1.1) 
      json_alerts = json.load(f)
    except JSONDecodeError:
      # Cannot load json this way, attempt to read by line instead
      retry_lines = True
      json_alerts = []
  if retry_lines:
    with open(filename) as f:
      for line in f:
        json_alerts.append(json.loads(line))
  # Create alert objects for all loaded json objects
  for json_alert in json_alerts:
    alert_obj = Alert(json_alert)
    alert_obj.file = filename
    alerts.append(alert_obj)
    if retry_lines:
        timestamps.append(json_alert['LogData']['DetectionTimestamp'][0])
    else:
        timestamps.append(json_alert['LogData']['Timestamps'][0])
  return alerts, timestamps
