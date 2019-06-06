from Table.HistoricalTable import HistoricalTable
from TraceInfo import TraceInfo
import os
import json
from pprint import pprint

# for tracking progress
from tqdm import tqdm

def make_database(trace_dir):
    """ Populate table using all traces located in trace_dir """
    contract_folders = [item for item in os.listdir(trace_dir)
            if os.path.isdir(os.path.join(trace_dir, item))]

    for address in tqdm(contract_folders, desc='Progress'):

        # Initialize table
        H = HistoricalTable()

        # Get all json files in that address folder
        address_path = os.path.join(trace_dir, address)
        all_jsons = [f for f in os.listdir(address_path) 
            if f.endswith('.json')]

        # Update table
        for json_file in tqdm(all_jsons, desc=f'Folder: {address}'):
            # Ignore creation.json and historical_table.json (if they exist)
            if json_file in ['creation.json', 'historical_table.json']:
                continue

            json_file_path = os.path.join(trace_dir, address, json_file)
            with open(json_file_path) as f:
                traces = json.load(f)

                for trace in tqdm(traces, desc=f'File: {json_file}'):
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
        
def main():
    make_database('trace_samples')

if __name__ == "__main__":
    main()
