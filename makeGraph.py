from Graph.GraphAggregator import GraphAggregator
from TraceInfo import TraceInfo
import os
import json
from pprint import pprint

# for tracking progress
from tqdm import tqdm

def makeGraph(trace_dir):
    """ Create json file representing directed, aggregated graph 
        of all execution paths in a contract folder. """
    contract_folders = [item for item in os.listdir(trace_dir)
            if os.path.isdir(os.path.join(trace_dir, item))]
    graph_filename = "graph.json"

    for address in tqdm(contract_folders, desc='Progress'):

        # Initialize graph and input list of all execution paths 
        G = GraphAggregator()
        execution_paths = []

        # Get all json files in that address folder
        address_path = os.path.join(trace_dir, address)
        all_jsons = [f for f in os.listdir(address_path) 
            if f.endswith('.json')]
        skipped_files = 0

        # Collect execution paths
        for json_file in tqdm(all_jsons, desc=f'Folder: {address}'):
            # Ignore json files that are not integers
            filename = json_file.split('.json')[0]
            if not str.isdigit(filename):
                skipped_files += 1
                continue

            json_file_path = os.path.join(trace_dir, address, json_file)
            with open(json_file_path) as f:
                traces = json.load(f)

                for trace in tqdm(traces, desc=f'File: {json_file}'):
                    # Extract info and store in graph
                    T = TraceInfo()
                    trace_info = T.get_trace_info(trace)

                    # Get execution paths
                    for subtrace in trace_info:
                        path_as_str = subtrace['path']
                        path_as_lst = [int(s) for s in path_as_str.split(',')]
                        execution_paths.append(path_as_lst)

        # Make Graph and save into folder
        G.make_graph(execution_paths)
        graph = G.get_graph()
        new_file_path = os.path.join(trace_dir, address, graph_filename)

        # Remove old table if it currently exists
        if os.path.isfile(new_file_path):
            os.remove(new_file_path)
            
        fn = open(new_file_path, 'w')
        json.dump(graph, fn)
        fn.close()
        print(f'\nGraph saved! {skipped_files} files skipped.')

    return

def main():
    makeGraph('trace_samples')

if __name__ == "__main__":
    main()