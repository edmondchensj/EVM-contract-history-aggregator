# EVM-graph-aggregator

## Objective
The graph aggregator takes in a list of execution paths (in terms of program counters) and outputs an aggregated directed graph. 

## Format
Input: A list of lists

Output: A dict of dicts of dict, where: 
    first level keys are source nodes,
    second level keys are the destination nodes,
    third level key is a fixed string ('constraint'),
    third level value is the subgraph of paths that the specific (source, destination) edge allows (a dict of dicts).  


### Example 
Input: 
`[[1, 2, 4, 5, 7, 8], [1, 3, 4, 6, 7, 9]]`

Output: 
`
{1: {2: {'constraint': {}}, 3: {'constraint': {}}},
 2: {4: {'constraint': {}}},
 3: {4: {'constraint': {}}},
 4: {5: {'constraint': {1: {2}}}, 6: {'constraint': {1: {3}}}},
 5: {7: {'constraint': {}}},
 6: {7: {'constraint': {}}},
 7: {8: {'constraint': {1: {2}, 4: {5}}}, 9: {'constraint': {1: {3}, 4: {6}}}}}
 `