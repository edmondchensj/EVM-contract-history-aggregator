from pprint import pprint
import copy

class GraphAggregator(object):

    def __init__(self):
        """ Initialize graphs. 
        Backup graph is used in make_graph() and update_old_branches(). """
        self.G = dict()
        self.G_backup = dict()

    def make_graph(self, list_of_paths, view_progress=True):
        """ Make Aggregated Graph from list of execution paths """

        for i, path in enumerate(list_of_paths):

            # No constraints required for first path
            if i == 0:
                self.add_all_edges(path)

            else:
                constraint = {}

                for (source, dest) in zip(path, path[1:]): 

                    # Add edge to graph if it is new
                    if not self.has_edge(source, dest):
                        self.add_edge(source, dest)

                    # Check if source node is a "branching" node
                    # i.e. has more than one destination node 
                    if len(self.G[source]) >= 2: 

                        # If path constraints exist, add to edge
                        if len(constraint) >= 1:

                            self.update_edge_constraint(source, dest, constraint)
                            self.update_old_branches(source, constraint)

                        # Add this edge to path constraints
                        constraint.update({source: {dest}})

            # Once path fully added, update backup copy of Graph
            self.G_backup = copy.deepcopy(self.G)

            # Show progress after each new path is added
            if view_progress:
                print('\nCurrent graph is: ')
                pprint(self.G)
                input("Press Enter to continue.\n")

    def update_old_branches(self, source, constraint):
        """ For each branch of a given source node, 
        find branches that currently have no constraints and 
        update its constraints based on constraints of a new path """
        for dest in self.G_backup[source]:
            for source_con, dest_con_set in constraint.items():
                # Skip if branch already has constraints
                if (source_con in self.G_backup[source][dest]['constraint']):
                    pass
                # Skip if constraint directly leads to the branching node
                elif (source in dest_con_set):
                    pass
                else: # Otherwise, update new graph with new constraints
                    self.G[source][dest]['constraint'].update({source_con: set(self.G_backup[source_con].keys())})

    def update_edge_constraint(self, source, dest, constraint):
        """ Update constraint for a given (source, dest) edge """
        for k, v in constraint.items():
            if k in self.G[source][dest]['constraint']:
                self.G[source][dest]['constraint'][k].update(v)
            else:
                self.G[source][dest]['constraint'].update({k: v})

    def add_all_edges(self, path):
        for (source, dest) in zip(path, path[1:]):
            self.add_edge(source, dest)

    def add_edge(self, source, dest):
        if source not in self.G:
            self.G[source] = {dest:{'constraint':{}}}
        else:
            self.G[source].update({dest:{'constraint':{}}})

    def has_edge(self, source, dest):
        return (source in self.G and dest in self.G[source])

    def get_graph(self):
        return self.G

def main(inputs):
    print('Inputs: ')
    pprint(inputs)
    print('\n')

    G = GraphAggregator()
    G.make_graph(inputs, view_progress=True)
    graph = G.get_graph()

    print('Final Graph: ')
    pprint(graph)

if __name__ == "__main__":
    test_inputs = [[1,2,4,5,7,8],
                [1,3,4,6,7,9],
                [1,3,4,5,7,8],
                [1,3,4,10,7,9],
                [1,3,11,4,10]]
    main(test_inputs)