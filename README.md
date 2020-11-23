# aecid-alert-aggregation
A method for grouping, clustering, and merging semi-structured alerts.

To get started, just clone this repository and execute
```
python3 aggregate.py
```
to run the aecid-alert-aggregation with the default input files and configurations. To change the configuration, edit the aggregate_config.py file.

When running the python script, the current status of the aggregation is printed on console. In its standard configuration, the script runs for several minutes and then outputs the generated meta-alerts in the directory specified in the configuration file. 

The directory 'samples' contains several examples that are useful for understanding the aggregation technique. The samples include:
* sample_similarity.py similarities of sample alerts
* sample_group_similarity.py similarities of sample alert groups
* sample_merge.py aggregation of sample alerts
* sample_group_merge.py aggregation of sample alert groups
* sample_hierarchical_clustering.py execution of the hierarchical clustering method on sample data
* sample.py execution of incremental meta-alert generation on sample data (corresponds to scenario 2 in paper)

The directory 'evaluation' contains several scripts that measure the performance of the approach. Note that the respective configurations are inside the scripts instead of the aggregate_config.py file. Evaluation scripts include:
* mds.py generates a similarity matrix for multi-dimensional scaling
* hierarchical_clustering.py generates an R script for plotting a dendrogram
* evaluate.py uses unsupervised clustering for meta-alert generation
* cross_validation.py uses supervised training for alert classification
* noise_evaluate.py measures the robustness of the approach

Copy any of the sample and evaluation scripts into the main directory to execute it, e.g.:
```
cp samples/sample.py ./sample.py
python3 sample.py
```

The output will be generated on the console or in the respective directory in data/out.

More information on the aecid-alert-aggregation is provided in the following paper:

Landauer M., Skopik F., Wurzenberger M., Rauber A.: Dealing with Security Alert Flooding: Using Machine Learning for Domain-independent Alert Aggregation. Under review.
