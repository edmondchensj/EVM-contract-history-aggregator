import json
from pprint import pprint

class TraceInfo(object):

    def __init__(self):
        self.visited_keys = {'mrd':[], 'srd':[]}

    def get_trace_info(self, trace):
        """ Helper function for extracting required information to check if a new contract call is an anomaly. 
        Given a trace (a dict), split up the execution path into no-loop paths and then
        get memory-read and storage-read dependencies for each path.

        Argument:
            trace -- a dict
        Returns: 
            list of dicts  
        """

        # Ignore failures
        if trace["success"] == False:
            return 

        full_path = trace['path']
        subpaths = self.preprocess_with_nonce(full_path) # convert path into multiple no-loop paths

        # Initialize output
        trace_info = []

        # Loop through path to get dependencies
        for i, path_with_nonce in enumerate(subpaths):
            path_info = {'path': [path_tuple[1] for path_tuple in path_with_nonce],
                    'mrd': None,
                    'srd': None}

            max_nonce = path_with_nonce[-1][0]    # path is ordered, so we use the final nonce of the path
            final_subpath = (i == (len(subpaths) - 1)) # check if we are on the final subpath
            path_info['mrd'] = self.get_dependencies(trace, 'mrd', max_nonce, final_subpath)
            path_info['srd'] = self.get_dependencies(trace, 'srd', max_nonce, final_subpath)
            trace_info.append(path_info)

        return trace_info

    def get_cti_relation(self, srd):
        """Copied from HistoricalTable class"""
        reader_cti = srd['reader']['cti']
        writer_ctis = [w['cti'] for w in srd['writers']]

        relations = []
        for w_cti in writer_ctis:
            if reader_cti == w_cti: 
                relations.append('self')

            elif len(reader_cti) < len(w_cti):
                if all(i in w_cti for i in reader_cti):
                    relations.append('child')
                else:
                    relations.append('else')

            else:
                if all(i in reader_cti for i in w_cti):
                    relations.append('parent')
                else:
                    relations.append('else')
        return relations

    def get_dependencies(self, trace, dep_type, max_nonce, final_subpath=False):
        """ Modified from HistoricalTable class.
        Gets memory-read dependencies (MRD) for a specific subpath (produced by preprocessing looped paths). 
        We assign these dependencies to subpaths using nonces. 
        We assign MRDs when nonce for that MRD is below the "max_nonce" for a subpath, 
            with the exception of the final subpath. 
        """
        dependencies = {}

        for dep in trace[dep_type]:
            # Skip dependencies that should not be allocated to this subpath
            # with exception for final subpath
            if dep['reader']['nonce'] >= max_nonce and not final_subpath:
                continue

            # Get key (reader pc)
            key = dep['reader']['pc']

            # Skip dependencies that have been assigned
            if key in self.visited_keys[dep_type]:
                continue
            else:
                self.visited_keys[dep_type].append(key)

            # Get value (writer pc and cti relation if applicable)
            writer_pcs =[w['pc'] for w in dep['writers']]
            if dep_type == 'mrd':
                val = writer_pcs
            elif dep_type == 'srd':
                relations = self.get_cti_relation(dep)
                val = [(pc, r) for pc, r in zip(writer_pcs, relations)]

            dependencies.update({key:val})

        return dependencies

    def preprocess_with_nonce(self, path_with_nonce):
        """ Convert paths with loops to no-loop paths 
        Input: list of (mutable) tuples e.g. [[nonce, pc], [...]] 
        Output: list of list of tuples of type (nonce, pc)
        """
        new_paths = []

        visited = []
        visited_pcs = []

        for (nonce, pc) in path_with_nonce:
            if pc in visited_pcs: # Loop found
                # Terminate path and add to new_paths
                new_path = visited + [(nonce, pc)]
                new_paths.append(new_path)

                # Unwind visited pcs
                node_idx = visited_pcs.index(pc)
                visited_pcs = visited_pcs[:node_idx+1]

                # Unwind visited nodes
                visited = visited[:node_idx+1]

            else:
                visited_pcs.append(pc)
                visited.append((nonce, pc))

        # Add completed path to new_paths
        new_paths.append(visited)

        return new_paths

def main():
    with open('samples/tracelist_withLoops.json', 'r') as f:
        input_json = json.load(f)

    trace_dict = input_json[0][0]
    print("Trace dict is: ")
    pprint(trace_dict)

    T = TraceInfo()

    trace_info = T.get_trace_info(trace_dict)
    print("\nTrace info is: ")
    pprint(trace_info)

if __name__ == "__main__":
    main()



