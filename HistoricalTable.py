from pprint import pprint
import json

class HistoricalTable(object):

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
                    for mrd in trace['mrd']:
                        mrd_key = mrd['reader']['pc']
                        mrd_val = [w['pc'] for w in mrd['writers']]
                        self.update_table(path_key, 'mrd_possibilities', mrd_key, mrd_val)


                # Update SRD
                if trace['srd'] is not None:
                    for srd in trace['srd']:
                        srd_key = srd['reader']['pc']
                        writer_pcs = [w['pc'] for w in srd['writers']]
                        relations = self.get_cti_relation(srd)
                        srd_val = [(pc, r) for pc, r in zip(writer_pcs, relations)]
                        self.update_table(path_key, 'srd_possibilities', srd_key, srd_val)

    def update_table(self, path_key, table, table_key, table_val):
        try: 
            if table_val in self.table[path_key]['srd'][table_key]: 
                pass # Avoid duplicates
            else: 
                self.table[path_key][table][table_key].append(table_val)
        except KeyError: # New entry to table
            self.table[path_key][table][table_key] = [table_val]

    def get_cti_relation(self, srd):
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

def main():
    with open('examples/tracelist.json', 'r') as f:
        input_json = json.load(f)

    print("Input json is: ")
    pprint(input_json)

    D = HistoricalTable()
    D.make_table(input_json)
    table = D.get_table()

    print("Historical Table is: ")
    pprint(table)

if __name__ == "__main__":
    main()
