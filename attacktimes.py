from datetime import datetime
from datetime import timezone

phase = {
'cup': {
    'nmap': [datetime(2020, 3, 4, 19, 17, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 18, 00).replace(tzinfo=timezone.utc)],
    'nikto': [datetime(2020, 3, 4, 19, 18, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 19, 00).replace(tzinfo=timezone.utc)],
    'vrfy': [datetime(2020, 3, 4, 19, 21, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 22, 00).replace(tzinfo=timezone.utc)],
    'hydra': [datetime(2020, 3, 4, 19, 25, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 31, 00).replace(tzinfo=timezone.utc)],
    'upload': [datetime(2020, 3, 4, 19, 32, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 33, 00).replace(tzinfo=timezone.utc)],
    'exploit': [datetime(2020, 3, 4, 19, 35, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 40, 00).replace(tzinfo=timezone.utc)]},
'spiral': {
    'nmap': [datetime(2020, 3, 4, 17, 57, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 17, 58, 00).replace(tzinfo=timezone.utc)],
    'nikto': [datetime(2020, 3, 4, 18, 1, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 17, 00).replace(tzinfo=timezone.utc)],
    'vrfy': [datetime(2020, 3, 4, 18, 19, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 20, 00).replace(tzinfo=timezone.utc)],
    'hydra': [datetime(2020, 3, 4, 18, 23, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 28, 00).replace(tzinfo=timezone.utc)],
    'upload': [datetime(2020, 3, 4, 18, 28, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 30, 00).replace(tzinfo=timezone.utc)],
    'exploit': [datetime(2020, 3, 4, 18, 33, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 38, 00).replace(tzinfo=timezone.utc)]},
'insect': {
    'nmap': [datetime(2020, 3, 4, 13, 51, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 13, 52, 00).replace(tzinfo=timezone.utc)],
    'nikto': [datetime(2020, 3, 4, 13, 54, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 14, 11, 00).replace(tzinfo=timezone.utc)],
    'vrfy': [datetime(2020, 3, 4, 14, 11, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 14, 12, 00).replace(tzinfo=timezone.utc)],
    'hydra': [datetime(2020, 3, 4, 14, 14, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 14, 17, 00).replace(tzinfo=timezone.utc)],
    'upload': [datetime(2020, 3, 4, 14, 18, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 14, 20, 00).replace(tzinfo=timezone.utc)],
    'exploit': [datetime(2020, 3, 4, 14, 24, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 14, 29, 00).replace(tzinfo=timezone.utc)]},
'onion': {
    'nmap': [datetime(2020, 3, 4, 18, 43, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 44, 00).replace(tzinfo=timezone.utc)],
    'nikto': [datetime(2020, 3, 4, 18, 46, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 47, 00).replace(tzinfo=timezone.utc)],
    'vrfy': [datetime(2020, 3, 4, 18, 49, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 50, 00).replace(tzinfo=timezone.utc)],
    'hydra': [datetime(2020, 3, 4, 18, 50, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 52, 00).replace(tzinfo=timezone.utc)],
    'upload': [datetime(2020, 3, 4, 18, 55, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 18, 56, 00).replace(tzinfo=timezone.utc)],
    'exploit': [datetime(2020, 3, 4, 19, 00, 00).replace(tzinfo=timezone.utc), datetime(2020, 3, 4, 19, 5, 00).replace(tzinfo=timezone.utc)]}}

def get_phase(scenario, time):
    p = ""
    for test_phase, interval in phase[scenario].items():
        if  interval[0].timestamp() < time < interval[1].timestamp():
            return test_phase
    return p
