from pprint import pprint
import json
from TraceInfo import TraceInfo

class HistoricalTable(object):
    """
    Creates database for all historical traces. 
    Takes in result from TraceInfo.py and populates database. 
    """

    def __init__(self):
        self.table = dict()

    def update_table(self, trace_info):
        # Ignore failed traces
        # TraceInfo handles failed cases by returning None
        if trace_info == None:
            return

        # Loop through each subtrace in trace_info 
        for trace in trace_info:
            path_key = trace['path']
            if path_key not in self.table.keys():
                self.table[path_key] = {'mrd_possibilities':{},
                                    'srd_possibilities':{}}

            # Update MRD
            for mrd_key, mrd_val in trace['mrd'].items():
                self.update_dependencies(path_key, 'mrd_possibilities', mrd_key, mrd_val)

            # Update SRD
            for srd_key, srd_val in trace['srd'].items():
                self.update_dependencies(path_key, 'srd_possibilities', srd_key, srd_val)

    def update_dependencies(self, path_key, dep, key, val):
        try: 
            if val in self.table[path_key][dep][key]: 
                pass # Avoid duplicates
            else: # Add value to existing list
                self.table[path_key][dep][key].append(val)
        except KeyError: # New entry to table
            self.table[path_key][dep][key] = [val]

    def get_table(self):
        return self.table
'''
class HistoricalTable_Old(object):
    """ 
    [OLD VERSION] This version only works for no-loop traces and does not require TraceInfo.py. 
    Database for aggregating all historical traces and the respective dependencies. """

    def __init__(self):
        self.table = dict()

    def make_table(self, input_json):
        for trace_list in input_json:
            for trace in trace_list:

                # Ignore traces that are not successful
                if trace['success'] == False:
                    continue

                # Initialize
                path = self.get_trace_path(trace)
                path_key = tuple(path) # make immutable 
                if path_key not in self.table.keys():
                    self.table[path_key] = {'mrd_possibilities':{},
                                        'srd_possibilities':{}}

                # Update MRD
                if trace['mrd'] is not None:
                    self.get_dependencies(trace, 'mrd', path_key)

                # Update SRD
                if trace['srd'] is not None:
                    self.get_dependencies(trace, 'srd', path_key)

    def get_dependencies(self, trace, dep_type, path_key=None):
        for dep in trace[dep_type]:
            dep_key = dep['reader']['pc']

            writer_pcs =[w['pc'] for w in dep['writers']]
            if dep_type == 'mrd':
                dep_val = writer_pcs
            elif dep_type == 'srd':
                relations = self.get_cti_relation(dep)
                dep_val = [(pc, r) for pc, r in zip(writer_pcs, relations)]

            self.update_table(path_key, f'{dep_type}_possibilities', dep_key, dep_val)

    def update_table(self, path_key, table, table_key, table_val):
        try: 
            if table_val in self.table[path_key][table][table_key]: 
                pass # Avoid duplicates
            else: 
                self.table[path_key][table][table_key].append(table_val)
        except KeyError: # New entry to table
            self.table[path_key][table][table_key] = table_val

    def get_cti_relation(self, srd):
        """ Compare ctis between reader and writers and determine relationship 
        e.g. [] is parent of [0] and [1], [0,1] is child of [0]. 
        Grandparents are considered parents. Similarly grandchildren are considered children. 
        """
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

    def get_trace_path(self, trace):
        path = [path_tuple[1] for path_tuple in trace['path']]
        return path

    def get_table(self):
        return self.table
'''

def main():
    trace_info = [{'mrd': {455: [4]}, 
  'path': '0, 11, 170, 340, 444, 11', 
  'srd': {}},
 {'mrd': {}, 
 'path': '0, 11, 558, 199', 
 'srd': {1296: [(1818, 'self')]}}]
    print("Input trace is: ")
    pprint(trace_info)

    D = HistoricalTable()
    D.update_table(trace_info)
    table = D.get_table()

    print("Historical Table is: ")
    pprint(table)

    """
    with open('samples/tracelist.json', 'r') as f:
        input_json = json.load(f)

    print("Input json is: ")
    pprint(input_json)

    D = HistoricalTable_Old()
    D.make_table(input_json)
    table = D.get_table()

    print("Historical Table is: ")
    pprint(table)

    for key in table.keys():
      if type(key) is not str:
        try:
          table[str(key)] = table[key]
        except:
          try:
            table[repr(key)] = table[key]
          except:
            pass
        del table[key]

    with open('result.json','w') as fp:
        json.dump(table, fp)
    """
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()
