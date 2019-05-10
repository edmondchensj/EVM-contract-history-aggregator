from pprint import pprint
from collections import defaultdict
import copy

class GraphAggregator(object):

    def __init__(self):
        self.G = dict()
        self.G_backup = dict()

    def make_graph(self, list_of_paths, view_progress=True):
        """ Make Aggregated Graph from list of execution paths """

        for i, path in enumerate(list_of_paths):

            # No constraints required for first path
            if i == 0:
                self.add_all_edges(path)

            else:
                # Initialize path constraints
                constraint = {}

                for (source, dest) in path: 

                    # Add edge to graph if it is new
                    if not self.has_edge(source, dest):
                        self.add_edge(source, dest)

                    # Check if source node is a "branching" node
                    # i.e. has more than one destination node 
                    if len(self.G[source]) >= 2: 

                        # If constraint exist, add to edge
                        if len(constraint) >= 1:

                            # Update path with constraint
                            self.update_constraint(source, dest, constraint)

                            # Update old branches
                            self.update_old_branches(source, constraint)

                        # Add branch to path constraint
                        constraint.update({source: {dest}})

            # Once path fully added, update backup copy of Graph
            self.G_backup = copy.deepcopy(self.G)

            # Show progress after each new path is added
            if view_progress:
                print('\nCurrent graph is: ')
                pprint(self.G)
                input("Press Enter to continue.\n")

    def update_old_branches(self, source, constraint):
        # Initialize variable to track new constraints for other branches
        constraint_otherBr = {}

        for dest in self.G_backup[source]:
            for source_con, dest_con in constraint.items():
                # Check if constraint already exists
                if source_con in self.G_backup[source][dest]['constraint']:
                    # If constraint for already exists, no need to update
                    pass
                else: # Otherwise, Add all old paths to constraint
                    self.G[source][dest]['constraint'].update({source_con: set(self.G_backup[source_con].keys())})

    def update_constraint(self, source, dest, constraint):
        for k, v in constraint.items():
            if k in self.G[source][dest]['constraint']:
                self.G[source][dest]['constraint'][k].update(v)
            else:
                self.G[source][dest]['constraint'].update({k: v})

    def add_all_edges(self, list_of_edges):
        for (source, dest) in list_of_edges:
            self.add_edge(source, dest)

    def add_edge(self, source, dest):
        if source not in self.G:
            self.G[source] = {dest:{'constraint':{}}}
        else:
            self.G[source].update({dest:{'constraint':{}}})

    def has_edge(self, source, dest):
        return (source in self.G and dest in self.G[source])

def main(inputs):
    print('Inputs: ')
    pprint(inputs)
    print('\n')

    G = GraphAggregator()
    G.make_graph(inputs, view_progress=True)

if __name__ == "__main__":
    inputs = [[(1,2),(2,4),(4,5),(5,7),(7,8)],
            [(1,3),(3,4),(4,6),(6,7),(7,9)]]
    main(inputs)