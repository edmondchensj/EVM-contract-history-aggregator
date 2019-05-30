# Historical Table and Graph Aggregator for EVM Project 
This repo is the final component of the Anomaly-based Detector for Northwestern University's EECS450 Final Project. 

## Overview 
This repo contains two groups of scripts:
1. Historical Table
    * HistoricalTable.py: Main script for storing execution paths and dependencies of historical traces.
    * TraceInfo.py: Helper script for extracting the execution path and dependencies for a given trace. 
2. Graph Aggregator 
    * GraphAggregator.py: To aggregate list of paths into a single directed graph
    * preprocessing.py: To run before GraphAggregator.py for preprocessing input paths
    * visualization.py: To run after GraphAggregator.py for visualizing the graph

The purpose of the historical table is to aggregate important information in all historical traces. It contains the execution paths (in terms of program counters) and the memory and storage read dependencies for each path. With this table, we would be able to detect whether a new execution path is normal or an anomaly. This achieves the big picture goal for the EVM project.

The purpose of graph aggregator is to create a single directed graph per contract such that we obtain a snapshot of all historical execution paths for each contract. This is helpful for analyzing case studies.

## Historical Table (HistoricalTable.py)
The historical table takes in a json file of traces and updates its database.

### Format
Input: A json file

Output: A dict of dicts, where: <br>
* first level keys are the execution paths as tuples,
* second level keys are 'mrd' (memory-read-dependencies) or 'srd' (storage-read-dependencies)
* second level values are the respective reader-writer dependency tables (dicts) for 'mrd' and 'srd'.

### Example
Input: 
```
[
  [
    {
      "cti": [],
      "address": "0xcac7000c7dbaa2e33af15325af5d435e011c7bdd",
      "success": true,
      "path": [[1,0],[8,11],[18,170],[39,340],[60,427],[111,557],[112,558],[117,199]],
      "mrd": [{"reader":{"nonce":66,"pc":455,"op":"MLOAD"},"writers":[{"nonce":3,"pc":4,"op":"MSTORE"}]}],
      "srd": [{"reader":{"cti":[],"nonce":122,"pc":1296},"writers":[{"cti":[],"nonce":115,"pc":1818}]}]
    }
  ]
]

```

Output: (Single Entry)
```
{(0, 11, 170, 340, 427, 557, 558, 199): {'mrd_possibilities': {455: [4]},
                                         'srd_possibilities': {1296: [(1818, 'self')]}}}
```

## Trace Information Extraction (TraceInfo.py)
This is a helper script for extracting the exection path and dependencies for a given trace, allowing the user to then check if these information has been previously recorded in the Historical Table. 

Given a trace, the script extracts the path, preprocesses it to no-loop paths, and assigns dependencies. 

### Format
Input: dict 

Output: list of dicts

### Example
Input:
```
{'address': '0xcac7000c7dbaa2e33af15325af5d435e011c7bdd',
 'cti': [],
 'mrd': [{'reader': {'nonce': 66, 'op': 'MLOAD', 'pc': 455},
          'writers': [{'nonce': 3, 'op': 'MSTORE', 'pc': 4}]}],
 'path': [[1, 0],
          [8, 11],
          [18, 170],
          [39, 340],
          [60, 444],
          [111, 11],
          [112, 558],
          [117, 199]],
 'srd': [{'reader': {'cti': [], 'nonce': 122, 'pc': 1296},
          'writers': [{'cti': [], 'nonce': 115, 'pc': 1818}]}],
 'success': True}
```

Output:
```
[{'mrd': {455: [4]}, 'path': [0, 11, 170, 340, 444, 11], 'srd': {}},
 {'mrd': {}, 'path': [0, 11, 558, 199], 'srd': {1296: [(1818, 'self')]}}]
```

## Graph Aggregator (GraphAggregator.py)
The graph aggregator takes in a list of execution paths (in terms of program counters) and outputs an aggregated directed graph. 

### Format
Input: A list of lists

Output: A dict of dicts of dict, where: <br>
* first level keys are source nodes, 
* second level keys are destination nodes,
* third level key is a fixed string ('constraint'),
* third level value is the subgraph of paths that the specific edge allows (a dict of dicts)<sup>1</sup>. <br>

<sup>1</sup>*Note: If a node does not exist as a key in the subgraph dict, all branches from that node are permitted paths. In addition, constraints are not added to non-branching edges since restrictions would be applied to earlier branching edges.*

### Examples
#### 1) Two inputs; multiple, non-consecutive branches; no loops
Input: 
```
[[1, 2, 4, 5, 7, 8], 
[1, 3, 4, 6, 7, 9]]
```
<img src="examples/input_1.png" width="40%">

Output: 
```
{1: {2: {'constraint': {}}, 3: {'constraint': {}}},
 2: {4: {'constraint': {}}},
 3: {4: {'constraint': {}}},
 4: {5: {'constraint': {1: {2}}}, 6: {'constraint': {1: {3}}}},
 5: {7: {'constraint': {}}},
 6: {7: {'constraint': {}}},
 7: {8: {'constraint': {1: {2}, 4: {5}}}, 9: {'constraint': {1: {3}, 4: {6}}}}}
 ```
 <img src="examples/output_1.png" width="50%">


#### 2) Five inputs; multiple branches with consecutive branching (nodes 1,3,4); no loops
Input:
```
[[1, 2, 4, 5, 7, 8],
 [1, 3, 4, 6, 7, 9],
 [1, 3, 4, 5, 7, 8],
 [1, 3, 4, 10, 7, 9],
 [1, 3, 11, 4, 10]]
```
<img src="examples/input_2.png" width="40%">


Output:
```
{1: {2: {'constraint': {}}, 3: {'constraint': {}}},
 2: {4: {'constraint': {}}},
 3: {4: {'constraint': {}}, 11: {'constraint': {1: {3}}}},
 4: {5: {'constraint': {1: {2, 3}, 3: {4}}},
     6: {'constraint': {1: {3}, 3: {4}}},
     10: {'constraint': {1: {3}, 3: {4}}}},
 5: {7: {'constraint': {}}},
 6: {7: {'constraint': {}}},
 7: {8: {'constraint': {1: {2, 3}, 4: {5}}},
     9: {'constraint': {1: {3}, 4: {10, 6}}}},
 10: {7: {'constraint': {}}},
 11: {4: {'constraint': {}}}}
```
<img src="examples/output_2.png" width="50%">


## Preprocessing (preprocess.py)
The algorithm assumes that paths do not contain no-loops. In order to generalize the algorithm to paths with loops, users can run preprocessing script to first "flatten" their input paths. This turns paths with loops into the no-loop versions.

### Example
Input: 
```
[[1,2,3,4,2,3,4,5,7,8,5,6,8,9]]
```
<img src="examples/preprocess_input.png" width="40%">

Output:
```
[[1, 2, 3, 4, 2], 
[1, 2, 3, 4, 5, 7, 8, 5], 
[1, 2, 3, 4, 5, 6, 8, 9]]
```
<img src="examples/preprocess_output.png" width="40%">

## Graph Visualization (visualization.py)
The graph visualization takes the output generated by graph aggregator as the input, and creates a digraph using the Graphviz package in python.

### Example
Input
```
{1: {2: {'constraint': {}}, 3: {'constraint': {}}},
 2: {4: {'constraint': {}}},
 3: {4: {'constraint': {}}, 11: {'constraint': {1: {3}}}},
 4: {5: {'constraint': {1: {2, 3}, 3: {4}}},
     6: {'constraint': {1: {3}, 3: {4}}},
     10: {'constraint': {1: {3}, 3: {4}}}},
 5: {7: {'constraint': {}}},
 6: {7: {'constraint': {}}},
 7: {8: {'constraint': {1: {2, 3}, 4: {5}}},
     9: {'constraint': {1: {3}, 4: {10, 6}}}},
 10: {7: {'constraint': {}}},
 11: {4: {'constraint': {}}}}
```
Output: <br>
<img src="examples/graph_visualization.png" width="40%">
