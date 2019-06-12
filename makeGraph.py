from Graph.GraphAggregator import GraphAggregator
from TraceInfo import TraceInfo
import os
import json
from pprint import pprint
import argparse

# for tracking progress
from tqdm import tqdm

def makeGraph(trace_dir, selected_contracts=None, verbose=True):
    """ Create json file representing directed, aggregated graph 
        of all execution paths in a contract folder. """
    if selected_contracts is None:
        selected_contracts = [item for item in os.listdir(trace_dir)
                if os.path.isdir(os.path.join(trace_dir, item))]
    graph_filename = "graph.json"

    for address in selected_contracts:

        # Progress
        if verbose:
            print(f'({i}/{len(selected_contracts)}) Folder: {address}')

        # Initialize graph and input list of all execution paths 
        G = GraphAggregator()
        execution_paths = []

        # Get all json files in that address folder
        address_path = os.path.join(trace_dir, address)
        all_jsons = [f for f in os.listdir(address_path) 
            if f.endswith('.json')]
        skipped_files = 0
        if verbose:
            print(f'Now in Folder: {address}')
        # Collect execution paths
        for json_file in all_jsons:

            # Progress
            if verbose:
                print(f'> ({i}/{len(all_jsons)}) Getting traces from {json_file}')

            # Ignore json files that are not integers
            filename = json_file.split('.json')[0]
            if not str.isdigit(filename):
                skipped_files += 1
                continue

            json_file_path = os.path.join(trace_dir, address, json_file)
            with open(json_file_path) as f:
                traces = json.load(f)

                for trace in traces:
                    # Extract info and store in graph
                    T = TraceInfo()
                    trace_info = T.get_trace_info(trace)

                    # Get execution paths
                    if trace_info is None: # failed traces
                        continue
                    for subtrace in trace_info:
                        path_as_str = subtrace['path']
                        path_as_lst = [int(s) for s in path_as_str.split(',')]
                        execution_paths.append(path_as_lst)

        # Make Graph and save into folder
        if verbose:
            print('Execution paths collected.') 
            print('Making graph (this might take a long time) ... ')
        G.make_graph(execution_paths)
        if verbose:
            print('Getting graph ... ')
        graph = G.get_graph()
        new_file_path = os.path.join(trace_dir, address, graph_filename)

        # Remove old table if it currently exists
        if os.path.isfile(new_file_path):
            os.remove(new_file_path)
            
        if verbose:
            print('Saving graph ... ')
        fn = open(new_file_path, 'w')
        json.dump(graph, fn)
        fn.close()
    return

def main(folder, selected_contracts, verbose):
    
    makeGraph(folder, selected_contracts, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate aggregated graph of execution paths for all/selected contracts')
    parser.add_argument('folder',
                    help='Path to directory containing contract folders')
    parser.add_argument('--selected_contracts',
                    dest='selected_contracts',
                    default=None,
                    help='Generate graph for selected contract addresses only. Please provide a list of strings. \
                    If not given, aggregated graphs will be generated for all contracts in the folder.')
    parser.add_argument('--quiet',
                    dest='verbose'
                    action='store_false',
                    default=True,
                    help='Turn off progress status notifications.'
    main(args.folder, args.selected_contracts, args.verbose)