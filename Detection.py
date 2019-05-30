import os, json



'''
Input:
[
  [
    {
      "cti": [],
      "address": "0xcac7000c7dbaa2e33af15325af5d435e011c7bdd",
      "success": true,
      "path": [[1,0],[8,11],[18,170],[39,340],[60,427],[111,557],[112,558],[117,199]],
      "mrd": [{"reader":{"nonce":66,"pc":455,"op":"MLOAD"},"writers":[{"nonce":3,"pc":4,"op":"MSTORE"}]}],
      "srd": [{"reader":{"cti":[],"nonce":122,"pc":1296},"writers":[{"cti":[],"nonce":115,"pc":1818}]}]
    }
  ]
]
Output:
{(0, 11, 170, 340, 427, 557, 558, 199): {'mrd_possibilities': {455: [4]},
                                         'srd_possibilities': {1296: [[1818, "self"]]}}}

'''

class Detection(object):
	"""docstring for TracePartitioner"""
	def __init__(self):
		super(Detection, self).__init__()
		self.traceDir = './trace-logs/traces'
		self.testDir = './trace-logs/testtraces'
		self.dirlist = [item for item in os.listdir(self.traceDir) if os.path.isdir(os.path.join(self.traceDir, item))]
		self.testlist = [item for item in os.listdir(self.testDir) if os.path.isdir(os.path.join(self.testDir, item))]

	def Detection(self, trace):

		address = trace['address']
		has_key = False
		data = None
		if address in self.dirlist:
			with open(os.path.join(self.traceDir,self.dirlist[self.dirlist.index(address)],'historical_table.json')) as json_file:  
				 data = json.load(json_file)

			path = [path_tuple[1] for path_tuple in trace['path']]
			path_key = str(tuple(path))
			for key in data.keys():
				if path_key == key:
					has_key = True
					for mrd_item in trace['mrd']:
						if mrd_item['reader']['pc'] not in data[key]['mrd_possibilities'].keys():
							return False
						else:
							for writer in mrd_item['writers']:
								if writer['pc'] not in data[key]['mrd_possibilities'][mrd_item['reader']['pc']]:
									return False

					for srd_item in trace['srd']:
						if srd_item['reader']['pc'] not in data[key]['srd_possibilities'].keys():
							return False
						else:
							for writer in srd_item['writers']:
								has_writer = False
								for writer_possibility in data[key]['srd_possibilities'][srd_item['reader']['pc']]:
									if writer['pc'] in writer_possibility:
										has_writer = True 
								if not has_writer:
									return False
					
			if not has_key:
				return False

		else:
			return False

		return True

	def DetectionAll(self):
		for test in self.testlist:
			data = None
			with open(os.path.join(self.testDir,test,'tracelist.json')) as json_file:  
				 data = json.load(json_file)
			for transaction in data:
				for trace in transaction:

					if not self.Detection(trace):
						print("Block ", test," has abnormal trace(s)")
					else:
						print("All the traces in ", test, " are normal")

def main():
	D = Detection()
	D.DetectionAll()

if __name__ == "__main__":
    main()





		


