import os, json
from TraceInfo import TraceInfo



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
{(0, 11, 170, 340, 427, 557, 558, 199): {'mrd_possibilities': {455: [[4]]},
                                         'srd_possibilities': {1296: [[[1818, "self"]]]}}}

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

			path_key = trace['path']
			
			
			for key in data.keys():

				
				if path_key == key:
					has_key = True
					for mrd_item in trace['mrd'].keys():
						

						if str(mrd_item) not in data[key]['mrd_possibilities'].keys():
							print("Abnormal in mrd reader")
							return False
						else:
							writer_list = trace['mrd'][mrd_item]
							
							if writer_list not in data[key]['mrd_possibilities'][str(mrd_item)]:
								print("Abnormal in mrd writer")
								return False

					for srd_item in trace['srd'].keys():
						if str(srd_item) not in data[key]['srd_possibilities'].keys():
							print("Abnormal in srd reader")
							return False
						else:
							writer_list = trace['srd'][srd_item]

							
							if writer_list not in data[key]['srd_possibilities'][str(srd_item)]:
								print("Abnormal in srd writer")
								return False
					
			if not has_key:
				print("Abnormal in path")
				return False

		else:
			print("Does not have such transaction")
			return False

		return True

	def DetectionAll(self):
		for test in self.testlist:
			data = None
			path = os.path.join(self.testDir,test,'tracelist.json')
			T = TraceInfo()
			trace_info = T.transfer(path)

			for trace in trace_info:

				if not self.Detection(trace):
					print("Block ", test," has abnormal trace(s)")
				else:
					print("All the traces in ", test, " are normal")

def main():
	D = Detection()
	D.DetectionAll()

if __name__ == "__main__":
    main()





		


