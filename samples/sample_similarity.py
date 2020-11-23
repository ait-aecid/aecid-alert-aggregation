from similarity.similarity import get_json_similarity
import json
from merging.objects import Wildcard
from merging.objects import Mergelist

def createOutput(j1, j2, w=None):
  print('Json1 = ' + str(j1))
  print('Json2 = ' + str(j2))
  print('Similarity = ' + str(get_json_similarity(j1, j2, w)) + ' (' + str(get_json_similarity(j2, j1, w)) + ')')
  print('')

base = """
{
  "A": "a",
  "B": 1,
  "C": [
    "c", 
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

j0 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Identical')
createOutput(json.loads(base), json.loads(j0))

j1 =  """
{
  "X": "x",
  "Y": [
    "c",
    1
  ],
  "Z": {
    "Z1": false
  }
}"""

print('Completely different')
createOutput(json.loads(base), json.loads(j1))

j2 =  """
{
  "A": "x",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Change A value')
createOutput(json.loads(base), json.loads(j2))

j3 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    2
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Change C list value')
createOutput(json.loads(base), json.loads(j3))

j4 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": false,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Change D subdict boolean value')
createOutput(json.loads(base), json.loads(j4))

j5 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "dx.y",
      "d2.3"
    ]
  }
}"""

print('Change D subdict array value')
createOutput(json.loads(base), json.loads(j5))

j6 =  """
{
  "A": "a",
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Missing B key value')
createOutput(json.loads(base), json.loads(j6))

j7 =  """
{
  "A": "a",
  "B": 1,
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Missing C key list')
createOutput(json.loads(base), json.loads(j7))

j8 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ]
}"""

print('Missing D key dict')
createOutput(json.loads(base), json.loads(j8))

j9 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Missing D key sub value')
createOutput(json.loads(base), json.loads(j9))

j10 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true
  }
}"""

print('Missing D key sub list')
createOutput(json.loads(base), json.loads(j10))

j11 =  """
{
  "A": [
    "a"
  ],
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Replace A value with list of same value')
createOutput(json.loads(base), json.loads(j11))

j12 =  """
{
  "A": [
    "b"
  ],
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Replace A value with list of different value')
createOutput(json.loads(base), json.loads(j12))

j13 =  """
{
  "A": "a",
  "B": 1,
  "C": {
    "c": 1
  },
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Replace C list with dictionary')
createOutput(json.loads(base), json.loads(j13))

j14 =  """
{
  "A": "a",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": 3
}"""

print('Replace D dict with value')
createOutput(json.loads(base), json.loads(j14))

j15 =  """
{
  "A": "x",
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Change A value weighted')
createOutput(json.loads(base), json.loads(j15), {'A': 0.5})

print('Wildcard A value')
j16_json = json.loads(base)
j16_json['A'] = Wildcard()
createOutput(json.loads(base), j16_json)

print('Wildcard D sublist')
j17_json = json.loads(base)
j17_json['D']['D2'] = Wildcard()
createOutput(json.loads(base), j17_json)

print('Mergelist C complete')
j18_json = json.loads(base)
j18_json['C'] = Mergelist([1, "abc", "c"])
createOutput(json.loads(base), j18_json)

print('Mergelist C incomplete')
j19_json = json.loads(base)
j19_json['C'] = Mergelist(["c"])
createOutput(json.loads(base), j19_json)

print('Mergelist D complete')
j20_json = json.loads(base)
j20_json['D']['D1'] = Mergelist([True, False])
createOutput(json.loads(base), j20_json)

print('Mergelist D incomplete')
j21_json = json.loads(base)
j21_json['D']['D1'] = Mergelist([False])
createOutput(json.loads(base), j21_json)

j22 =  """
{
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Wildcard A value missing')
j22_json = json.loads(base)
j22_json['A'] = Wildcard()
createOutput(json.loads(j22), j22_json)

j23 =  """
{
  "B": 1,
  "C": [
    "c",
    1
  ],
  "D": {
    "D1": true,
    "D2": [
      "d2.1",
      "d2.2",
      "d2.3"
    ]
  }
}"""

print('Mergelist A value missing')
j23_json = json.loads(base)
j23_json['A'] = Mergelist(["a"])
createOutput(json.loads(j23), j23_json)

print('Mergelist C no match')
j24_json = json.loads(base)
j24_json['C'] = Mergelist(["x"])
createOutput(json.loads(base), j24_json)

print('Mergelist C list')
j25_json = json.loads(base)
j25_json['C'] = Mergelist([['c', 1], ['c', 2]])
createOutput(json.loads(base), j25_json)

print('Mergelist C partial two')
j26_json = json.loads(base)
j26_json['C'] = Mergelist([["c", "a"], ["c", "b"]])
createOutput(json.loads(base), j26_json)

print('Mergelist C partial one')
j27_json = json.loads(base)
j27_json['C'] = Mergelist([["c", "a"], ["d", "b"]])
createOutput(json.loads(base), j27_json)

print('Mergelist C partial mixed')
j28_json = json.loads(base)
j28_json['C'] = Mergelist([["c", "a"], [1, 2]])
createOutput(json.loads(base), j28_json)

j29 = """
{
  "AnalysisComponent": {
    "AnalysisComponentIdentifier": 5,
    "AnalysisComponentType": "NewMatchPathValueDetector",
    "AnalysisComponentName": "Exim no host name found ip",
    "Message": "New value(s) detected",
    "PersistenceFileName": "exim_no_host_name_found_ip",
    "AffectedLogAtomPaths": [
      "/parser/model/fm/no_host_found/ip"
    ],
    "AffectedLogAtomValues": [
      3232238161
    ],
    "ParsedLogAtom": {
      "/parser/model": "2020-03-04 18:19:49 no host name found for IP address 192.168.10.81",
      "/parser/model/time": 1583345989,
      "/parser/model/sp": " ",
      "/parser/model/fm/no_host_found": "no host name found for IP address 192.168.10.81",
      "/parser/model/fm/no_host_found/no_host_found_str": "no host name found for IP address ",
      "/parser/model/fm/no_host_found/ip": 3232238161
    }
  },
  "LogData": {
    "RawLogData": [
      "2020-03-04 18:19:49 no host name found for IP address 192.168.10.81"
    ],
    "Timestamps": [
      1583345989
    ],
    "LogLinesCount": 1
  }
}
"""

j30 = """
{
  "AnalysisComponent": {
    "AnalysisComponentIdentifier": 5,
    "AnalysisComponentType": "NewMatchPathValueDetector",
    "AnalysisComponentName": "Exim no host name found ip",
    "Message": "New value(s) detected",
    "PersistenceFileName": "exim_no_host_name_found_ip",
    "AffectedLogAtomPaths": [
      "/parser/model/fm/no_host_found/ip"
    ],
    "AffectedLogAtomValues": [
      3232238318
    ],
    "ParsedLogAtom": {
      "/parser/model": "2020-03-04 19:21:55 no host name found for IP address 192.168.10.238",
      "/parser/model/time": 1583349715,
      "/parser/model/sp": " ",
      "/parser/model/fm/no_host_found": "no host name found for IP address 192.168.10.238",
      "/parser/model/fm/no_host_found/no_host_found_str": "no host name found for IP address ",
      "/parser/model/fm/no_host_found/ip": 3232238318
    }
  },
  "LogData": {
    "RawLogData": [
      "2020-03-04 19:21:55 no host name found for IP address 192.168.10.238"
    ],
    "Timestamps": [
      1583349715
    ],
    "LogLinesCount": 1
  }
}
"""

print('AMiner alerts similarity')
createOutput(json.loads(j29), json.loads(j30), {'Timestamps': 0.0})

print('Nested lists')
j29_json_a = json.loads(base)
j29_json_a['C'] = ['c', ['a', 3]]
j29_json_b = json.loads(base)
j29_json_b['C'] = ['c', ['a', 4]]
createOutput(j29_json_a, j29_json_b)

print('Nested Mergelists')
j30_json_a = json.loads(base)
j30_json_a['C'] = ['c', ['a', 3]]
j30_json_b = json.loads(base)
j30_json_b['C'] = Mergelist([["c", "a"], [1, ['a', 2]]])
createOutput(j30_json_a, j30_json_b)

j31 = """{"timestamp":"2020-03-04T19:26:05.000000+0000","rule":{"level":5,"description":"PAM: User login failed.","id":"5503","firedtimes":28,"mail":false,"groups":["pam","syslog","authentication_failed"],"pci_dss":["10.2.4","10.2.5"],"gpg13":["7.8"],"gdpr":["IV_35.7.d","IV_32.2"]},"agent":{"id":"000","name":"user-0"},"manager":{"name":"user-0"},"id":"1587996038.9053510","full_log":"Mar  4 19:26:05 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=daryl rhost=127.0.0.1  user=daryl","predecoder":{"program_name":"auth","timestamp":"Mar  4 19:26:05","hostname":"mail"},"decoder":{"name":"pam"},"data":{"srcip":"127.0.0.1","srcuser":"daryl","dstuser":"daryl","uid":"0","euid":"0","tty":"dovecot"},"location":"/var/log/forensic/auth.log"}"""

j32 = """
{
        "AnalysisComponent": {
            "AnalysisComponentIdentifier": 4,
            "AnalysisComponentType": "NewMatchPathValueDetector",
            "AnalysisComponentName": "Apache user agent",
            "Message": "New value(s) detected",
            "PersistenceFileName": "apache_user_agent",
            "AffectedLogAtomPaths": [
                "/parser/model/combined/combined/user_agent"
            ],
            "AffectedLogAtomValues": [
                "Mozilla/5.0 (Hydra)"
            ],
            "ParsedLogAtom": {
                "/parser/model": "192.168.10.238 - - [04/Mar/2020:19:25:46 +0000] GET /login.php HTTP/1.0 200 6335 - Mozilla/5.0 (Hydra)",
                "/parser/model/client_ip/client_ip": 3232238318,
                "/parser/model/sp1": " ",
                "/parser/model/client_id": "-",
                "/parser/model/sp2": " ",
                "/parser/model/user_id": "-",
                "/parser/model/sp3": " [",
                "/parser/model/time": 1583349946,
                "/parser/model/sp4": " +",
                "/parser/model/tz": 0,
                "/parser/model/sp5": "] ",
                "/parser/model/request": "GET /login.php HTTP/1.0",
                "/parser/model/sp6": " ",
                "/parser/model/status_code": 200,
                "/parser/model/sp7": " ",
                "/parser/model/content_size": 6335,
                "/parser/model/combined": " - Mozilla/5.0 (Hydra)",
                "/parser/model/combined/combined": " - Mozilla/5.0 (Hydra)",
                "/parser/model/combined/combined/sp8": " ",
                "/parser/model/combined/combined/referer": "-",
                "/parser/model/combined/combined/sp9": " ",
                "/parser/model/combined/combined/user_agent": "Mozilla/5.0 (Hydra)",
                "/parser/model/combined/combined/sp10": ""
            }
        },
        "LogData": {
            "RawLogData": [
                "192.168.10.238 - - [04/Mar/2020:19:25:46 +0000] GET /login.php HTTP/1.0 200 6335 - Mozilla/5.0 (Hydra)"
            ],
            "Timestamps": [
                1583349946
            ],
            "LogLinesCount": 1
        }
    }
"""

print('AMiner and OSSEC alert similarity')
createOutput(json.loads(j31), json.loads(j32), {'Timestamps': 0.0, 'timestamp': 0.0})

j33 = """{"timestamp":"2020-03-04T19:25:47.000000+0000","rule":{"level":5,"description":"PAM: User login failed.","id":"5503","firedtimes":1,"mail":false,"groups":["pam","syslog","authentication_failed"],"pci_dss":["10.2.4","10.2.5"],"gpg13":["7.8"],"gdpr":["IV_35.7.d","IV_32.2"]},"agent":{"id":"000","name":"user-0"},"manager":{"name":"user-0"},"id":"1587996020.9004497","full_log":"Mar  4 19:25:47 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=daryl rhost=127.0.0.1  user=daryl","predecoder":{"program_name":"auth","timestamp":"Mar  4 19:25:47","hostname":"mail"},"decoder":{"name":"pam"},"data":{"srcip":"127.0.0.1","srcuser":"daryl","dstuser":"daryl","uid":"0","euid":"0","tty":"dovecot"},"location":"/var/log/forensic/auth.log"}
"""

j34 = """{"timestamp":"2020-03-04T19:25:48.000000+0000","rule":{"level":5,"description":"PAM: User login failed.","id":"5503","firedtimes":2,"mail":false,"groups":["pam","syslog","authentication_failed"],"pci_dss":["10.2.4","10.2.5"],"gpg13":["7.8"],"gdpr":["IV_35.7.d","IV_32.2"]},"agent":{"id":"000","name":"user-0"},"manager":{"name":"user-0"},"id":"1587996020.9004942","full_log":"Mar  4 19:25:48 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=daryl rhost=127.0.0.1  user=daryl","predecoder":{"program_name":"auth","timestamp":"Mar  4 19:25:48","hostname":"mail"},"decoder":{"name":"pam"},"data":{"srcip":"127.0.0.1","srcuser":"daryl","dstuser":"daryl","uid":"0","euid":"0","tty":"dovecot"},"location":"/var/log/forensic/auth.log"}
"""

print('OSSEC same alert type similarity')
createOutput(json.loads(j33), json.loads(j34), {'Timestamps': 0.0, 'timestamp': 0.0})

j35 = """{"timestamp":"2020-03-04T18:26:40.000000+0000","rule":{"level":10,"description":"PAM: Multiple failed logins in a small period of time.","id":"5551","frequency":6,"firedtimes":22,"mail":false,"groups":["pam","syslog","authentication_failures"],"pci_dss":["10.2.4","10.2.5","11.4"],"gpg13":["7.8"],"gdpr":["IV_35.7.d","IV_32.2"]},"agent":{"id":"000","name":"user-0"},"manager":{"name":"user-0"},"id":"1588006002.10530551","previous_output":"Mar  4 18:26:23 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:23 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:22 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:22 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:22 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:22 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanniMar  4 18:26:22 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanni","full_log":"Mar  4 18:26:40 mail auth: pam_unix(dovecot:auth): authentication failure; logname= uid=0 euid=0 tty=dovecot ruser=giovanni rhost=127.0.0.1  user=giovanni","predecoder":{"program_name":"auth","timestamp":"Mar  4 18:26:40","hostname":"mail"},"decoder":{"name":"pam"},"data":{"srcip":"127.0.0.1","srcuser":"giovanni","dstuser":"giovanni","uid":"0","euid":"0","tty":"dovecot"},"location":"/var/log/forensic/auth.log"}
"""

print('OSSEC similar alert type similarity')
createOutput(json.loads(j33), json.loads(j35), {'Timestamps': 0.0, 'timestamp': 0.0})

j36 = """{"timestamp":"2020-03-04T19:25:23.619885+0000","rule":{"level":6,"description":"IDS event.","id":"20101","firedtimes":1918,"mail":false,"groups":["ids"]},"agent":{"id":"000","name":"user-0"},"manager":{"name":"user-0"},"id":"1587995996.9002955","full_log":"03/04/2020-19:25:23.619885  [**] [1:2012887:3] ET POLICY Http Client Body contains pass= in cleartext [**] [Classification: Potential Corporate Privacy Violation] [Priority: 1] {TCP} 192.168.10.190:43332 -> 192.168.10.154:80","predecoder":{"timestamp":"03/04/2020-19:25:23.619885"},"decoder":{"parent":"snort","name":"snort"},"data":{"srcip":"192.168.10.190","dstip":"192.168.10.154:80","id":"1:2012887:3"},"location":"/var/log/forensic/suricata/fast.log"}"""

print('OSSEC different alert type similarity')
createOutput(json.loads(j33), json.loads(j36), {'Timestamps': 0.0, 'timestamp': 0.0})

j37 = """
{
  "A": "a",
  "B": "b1",
  "C": ["c1", "c2"],
  "D": {
    "D1": "d1",
    "D2": "d2"
  },
  "E": "e2",
  "F": "f4",
  "G": "g8"
}"""

j38 =  """
{
  "A": "a",
  "B": "b2",
  "C": ["c1"],
  "D": {
    "D1": "d1"
  },
  "E": "replace_with_mergelist",
  "F": "replace_with_mergelist",
  "G": "replace_with_wildcard"
}"""

print('Sample for presentation')
j38_json = json.loads(j38)
j38_json["E"] = Mergelist(["e1", "e2", "e3"])
j38_json["F"] = Mergelist(["f1", "f2", "f3"])
j38_json["G"] = Wildcard()
createOutput(json.loads(j37), j38_json)
