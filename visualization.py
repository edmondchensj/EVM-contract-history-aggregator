from graphviz import Digraph
from pprint import pprint
from GraphAggregator import GraphAggregator

def test():


	dot = Digraph(comment='The Round Table')

	dot.node('1','1')
	dot.node('2','2')
	dot.node('11','11')

	#dot.edges(['a1a2','a2a11'])
	dot.edge('1', '2', constraint='true')
	dot.edge('2', '11', constraint='true')


	dot.view()


def getGraph(output):
	dot = Digraph(comment='Graph Aggregator')
	nodes = []
	
	for key in output.keys():
		if key not in nodes:
			nodes.append(str(key))
		for sub_key in output[key].keys():
			if sub_key not in nodes:
				nodes.append(str(sub_key))
			
	for key in  output.keys():
		for sub_key in output[key].keys():
			if output[key][sub_key]['constraint']:

				dot.node(str(sub_key), str(sub_key), xlabel=str(output[key][sub_key]['constraint']))
				nodes.remove(str(sub_key))

	for i in nodes:
		dot.node(i, i)
	for key in output.keys():
		for sub_key in output[key].keys():
			# if output[key][sub_key]['constraint']:
			dot.edge(str(key),str(sub_key), constraint='true')
			# else:
			# 	dot.edge(str(key),str(sub_key), constraint='false')


	dot.render('test-output/graph-aggregator.gv', view=True)  
	


def main():
	test_inputs = [[1,2,4,5,7,8],
				[1,3,4,6,7,9],
				[1,3,4,5,7,8],
				[1,3,4,10,7,9],
				[1,3,11,4,10]]
				
	G = GraphAggregator()
	G.make_graph(test_inputs, view_progress=True)
	graph = G.get_graph()
	print("Final graph: ")
	pprint(graph)

	getGraph(graph)


if __name__ == '__main__':
	# This is the `main` call in python
	main()



