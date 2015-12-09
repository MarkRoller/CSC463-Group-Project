# # #
# Takes graphs in a file and compiles comparative information on them
#
# Usage: python NetworkAnalyzer.py <filename>
#
# @version 1 - Modified December 8 2015 11:22 AM
# @python-version 2.7
# #

import sys

def PowerControl(network,numNodes):

	for line in network:
		print line

	# dictionary of nodes and their transmitting power 
	nodes = {}
	for row in range(0,numNodes):
		nodes[row] = 0

	for row in range(1,numNodes):
		for col in range(0,row):
			print network[row][col]
			if network[row][col] == 1:
				if network[col][row] > nodes[row]:
					nodes[row] = network[col][row]

			if network[row][col] == -1:
				if network[col][row] > nodes[col]:
					nodes[col] = network[col][row]
				
	print nodes


	# for each node entry in the dictionary, check to see if it is transmitting 
	for entry in nodes:
		receiving = []
		# if a node entry has a value of 0, then the node is not transmitting
		if nodes[entry] == 0:
			continue
		else:
			# the node is transmitting and here is where we have to do the comparisons	
			for row in range(1,numNodes):	
				if network[row][entry] == -1:
					receiving.append(row)
			for col in range(0,entry):
				if network[entry][col] == 1:
					receiving.append(col)


		print "receiving"
		print receiving				
		
		for y in receiving:
			nodes_reached = []
			for x in nodes:
				if nodes[x] == 0:
					continue
				print "network entry x"
				print network[x][y]
				print "node entry"
				print nodes[x]
				if network[x][y] <= nodes[x]:
				# the node is within reach	
					if x == y:
						continue
					nodes_reached.append(x)
		print "nodes reached just to see"
		print nodes_reached

		#print receiving




	return "end of function"	

				# TODO:
				# Add to dict
				# Go through and compare power/noise
				# Return yes/no

def RegularControl(network,numNodes):
	for col in range(0,numNodes-2):
		for row in range(1,numNodes-1):
			if network[row][col] == 1:
				dummyVariable = 0

				# TODO:
				# Add to dict
				# Go through and compare power/noise
				# Return yes/no

def Processor(inputs):
	try:
		fileName = inputs[0]
	except:
		print("Missing Input.")
		sys.exit(1)

	with open("./" + fileName, "r") as inputFile:
		with open("./" + fileName.split(".")[0] + "_Output.txt", "w") as outputFile:

			getNodes = 0
			for line in inputFile:
				if getNodes == 0:
					numNodes = int(line.split("\n")[0])
					inMatrix = [[0 for x in range(numNodes)] for x in range(numNodes)]
					getNodes = 1
					rowPosition = 0
					continue

				if line.split("\n")[0] == "<end>":
					getNodes = 0
					print PowerControl(inMatrix,numNodes)
					regularResult = RegularControl(inMatrix,numNodes)

					# TODO: ADD OUTPUT TO FILE
					continue

				colPosition = 0
				for value in line.split("\n")[0].split(","):
					inMatrix[rowPosition][colPosition] = int(value)
					colPosition = colPosition+1
				rowPosition = rowPosition+1


if __name__ == '__main__':
    Processor(sys.argv[1:])
