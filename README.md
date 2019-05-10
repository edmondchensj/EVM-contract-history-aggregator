# EVM-graph-aggregator

## Objective
The graph aggregator takes in a list of execution paths (in terms of program counters) and outputs an aggregated directed graph. 

## Format
Input: A list of lists

Output: A dict of dicts of dict, where: <br>
* first level keys are source nodes, 
* second level keys are destination nodes,
* third level key is a fixed string ('constraint'),
* third level value is the subgraph of paths that the specific edge allows (a dict of dicts)<sup>1</sup>. <br>

<sup>1</sup>*Note: If a node does not exist as a key in the subgraph dict, all branches from that node are permitted paths. In addition, constraints are not added to non-branching edges since restrictions would be applied to earlier branching edges.* 


## Examples
### 1) Two inputs; multiple, non-consecutive branches; no loops
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
 <img src="examples/output_1.png" width="70%">


### 2) Five inputs; multiple branches with consecutive branching (nodes 1,3,4); no loops
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
<img src="examples/output_2.png" width="70%">
