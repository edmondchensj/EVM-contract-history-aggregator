from Table.HistoricalTable import HistoricalTable
from TraceInfo import TraceInfo
import os
import json
from pprint import pprint
import argparse

def make_database(trace_dir, selected_contracts=None, verbose=True):
    """ Populate table using all traces located in trace_dir """
    if selected_contracts is None:
        selected_contracts = [item for item in os.listdir(trace_dir)
                if os.path.isdir(os.path.join(trace_dir, item))]

    for i, address in enumerate(selected_contracts):

        # Progress
        if verbose:
            print(f'({i}/{len(selected_contracts)}) Folder: {address}')

        # Initialize table
        H = HistoricalTable()

        # Get all json files in that address folder
        address_path = os.path.join(trace_dir, address)
        all_jsons = [f for f in os.listdir(address_path) 
            if f.endswith('.json')]

        # Update table
        for j, json_file in enumerate(all_jsons):

            # Progress
            if verbose:
                print(f'> ({i}/{len(all_jsons)}) Getting traces from {json_file}')

            # Ignore creation.json and historical_table.json (if they exist)
            if json_file in ['creation.json', 'historical_table.json']:
                continue

            json_file_path = os.path.join(trace_dir, address, json_file)
            with open(json_file_path) as f:
                traces = json.load(f)

                for trace in traces:
                    # Extract info and store in table
                    T = TraceInfo()
                    trace_info = T.get_trace_info(trace)
                    H.update_table(trace_info)

        # Save table in the address folder
        table = H.get_table()
        new_file_path = os.path.join(trace_dir, address, "historical_table.json")

        # Remove old table if it currently exists
        if os.path.isfile(new_file_path):
            os.remove(new_file_path)

        fn = open(new_file_path, 'w')
        json.dump(table, fn)
        fn.close()
        
def main(folder, selected_contracts, verbose):
    make_database(folder, selected_contracts, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate aggregated database for all/selected contracts')
    parser.add_argument('folder',
                    help='Path to directory containing contract folders')
    parser.add_argument('--selected_contracts',
                    dest='selected_contracts',
                    default=None,
                    help='Generate database for selected contract addresses only. Please provide a list of strings. \
                    If not given, aggregated database will be generated for all contracts in the folder.')
    parser.add_argument('--quiet',
                    dest='verbose'
                    action='store_false',
                    default=True,
                    help='Turn off progress status notifications.'
    main(args.folder, args.selected_contracts, args.verbose)
