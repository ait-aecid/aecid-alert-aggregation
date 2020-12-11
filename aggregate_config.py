# Specifies the input data, where it is possible to use multiple alert sources (IDS) running on the same system in parallel, and arbitrary many systems, e.g.,
# files = [[system_A_ids_1, system_A_ids_2], [system_B_ids_1, system_B_ids_2, system_B_ids_3, ...], ...]
# For a single file, just use files = [['path_to_file']]
files = [['data/ossec/ossec_cup.json', 'data/aminer/aminer_cup.txt'], ['data/ossec/ossec_onion.json', 'data/aminer/aminer_onion.txt'], ['data/ossec/ossec_insect.json', 'data/aminer/aminer_insect.txt'], ['data/ossec/ossec_spiral.json', 'data/aminer/aminer_spiral.txt']]

input_type = None # Supports 'aminer' or 'ossec'. If None, automatically selects correct parser based on input file directory.
deltas = [0.5, 5] # Delta time intervals for group formation in seconds.
threshold = 0.3 # Minimum group similarity threshold for incremental clustering [0, 1].
min_alert_match_similarity = None # Minimum alert similarity threshold for group matching [0,1]. Set to None to use same value as threshold.
max_val_limit = 10 # Maximum number of values in merge lists before they are replaced by wildcards [0, inf].
min_key_occurrence = 0.1 # Minimum relative occurrence frequency of attributes to be included in merged alerts [0, 1].
min_val_occurrence = 0.1 # Minimum relative occurrence frequency of attribute values to be included in attributes of merged alerts [0, 1].
alignment_weight = 0.1 # Influence of alignment on group similarity [0, 1].
max_groups_per_meta_alert = 25 # Maximum queue size [1, inf]. Set to None for unlimited queue size.
queue_strategy = 'logarithmic' # Queue storage strategy, supported strategies are 'linear' and 'logarithmic'.
w = {'timestamp': 0, 'Timestamp': 0, 'timestamps': 0, 'Timestamps': 0} # Attribute weights used in alert similarity computation. It is recommended to set the weights of timestamps to 0.
output_dir = 'data/out/aggregate/meta_alerts.txt' # Directory where meta-alerts are stored.
output_alerts = True # Specifies whether alerts are printed to file.
output_alerts_dir = 'data/out/aggregate/alerts.txt' # Directory where alerts from input files are stored. 
