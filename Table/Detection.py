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
		self.testDir = './trace-logs/testrawtraces'
		self.dirlist = [item for item in os.listdir(self.traceDir) if os.path.isdir(os.path.join(self.traceDir, item))]
		self.testlist = [item for item in os.listdir(self.testDir) if os.path.isdir(os.path.join(self.testDir, item))]
		self.normal = 0
		self.abnormal = 0
		self.missing = 0
		self.blocknumber = 0
		self.tracenumber = 0
		self.result = {}
		self.ab0 = 0
		self.ab1 = 0
		self.ab2 = 0
		self.ab3 = 0
		self.ab4 = 0

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
							error = str(self.blocknumber) + ' ' + "trace " + str(self.tracenumber)
							error_text = 'Abnormal in mrd reader'
							self.result[error] = error_text
							self.abnormal += 1
							self.ab0 += 1
							print("Abnormal in mrd reader")
							return False
						else:
							writer_list = trace['mrd'][mrd_item]
							
							if writer_list not in data[key]['mrd_possibilities'][str(mrd_item)]:
								error = str(self.blocknumber) + ' ' + "trace " + str(self.tracenumber)
								error_text = 'Abnormal in mrd writer'
								self.result[error] = error_text
								self.abnormal += 1
								self.ab1 += 1
								print("Abnormal in mrd writer")
								return False

					for srd_item in trace['srd'].keys():
						if str(srd_item) not in data[key]['srd_possibilities'].keys():
							error = str(self.blocknumber) + ' ' + "trace " + str(self.tracenumber)
							error_text = 'Abnormal in srd reader'
							self.result[error] = error_text
							self.abnormal += 1
							self.ab2 += 1
							print("Abnormal in srd reader")
							return False
						else:
							writer_list = trace['srd'][srd_item]

							
							if writer_list not in data[key]['srd_possibilities'][str(srd_item)]:
								error = str(self.blocknumber) + ' ' + "trace " + str(self.tracenumber)
								error_text = 'Abnormal in srd writer'
								self.result[error] = error_text
								self.abnormal += 1
								self.ab3 += 1
								print("Abnormal in srd writer")
								return False
					
			if not has_key:
				error = str(self.blocknumber) + ' ' + "trace " + str(self.tracenumber)
				error_text = 'Abnormal in path'
				self.result[error] = error_text
				self.abnormal += 1
				self.ab4 += 1
				print("Abnormal in path")
				return False

		else:
			self.missing += 1
			print("Does not have such transaction")
			return False

		self.normal += 1

		return True

	def DetectionAll(self):
		count = 0
		for test in self.testlist:
			self.blocknumber = test
			data = None
			path = os.path.join(self.testDir,test,'tracelist.json')
			T = TraceInfo()
			trace_info = T.transfer(path)

			if trace_info:

				self.tracenumber = 0


				for trace in trace_info:
					self.tracenumber += 1
					count += 1

					if not self.Detection(trace):
						print("Block ", test," has abnormal trace(s)")
					else:
						print("All the traces in ", test, " are normal")

			# data = {}
			# data['total test traces'] = count
			# data['normal traces'] = self.normal
			# data['abnormal traces'] = self.abnormal
			# data['missing traces'] = self.missing
			
		self.result['normal traces rate'] = float(self.normal/count)
		self.result['abnormal traces rate'] = float(self.abnormal/count)
		self.result['missing traces rate'] = float(self.missing/count)
		self.result['Abnormal in path rate'] = float(self.ab4/self.abnormal)
		self.result['Abnormal in mrd reader rate'] = float(self.ab0/self.abnormal)
		self.result['Abnormal in mrd writer rate'] = float(self.ab1/self.abnormal)
		self.result['Abnormal in srd reader rate'] = float(self.ab2/self.abnormal)
		self.result['Abnormal in srd writer rate'] = float(self.ab3/self.abnormal)
		with open('results.json', 'w') as outfile:
			# json.dump(data, outfile)
			json.dump(self.result, outfile, indent=1)

def main():
	D = Detection()
	D.DetectionAll()

if __name__ == "__main__":
    main()





		


