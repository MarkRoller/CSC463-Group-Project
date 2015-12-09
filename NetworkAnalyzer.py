# # #
# Takes graphs in a file and compiles comparative information on them
#
# Usage: python NetworkAnalyzer.py <filename>
#
# @version 1 - Modified December 8 2015 11:22 AM
# @python-version 2.7
# #

import sys
import numpy as np
import itertools
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

def GeneratePaths(distances,minPower,start,end, numNodes):
	#Just going to create a matrix of all possible paths
	matrix = [x for x in range(numNodes)]
	#print matrix
	allPossiblePaths = []
	allPossiblePaths.append(itertools.permutations(matrix))
	allPossiblePaths = list(itertools.permutations(matrix, len(matrix)))
	shortestDistance = 9999999999999
	shortestPath = []
	#print allPossiblePaths

	for row in allPossiblePaths:
		#row = np.array(row)
		startPos = row.index(start)
		endPos = row.index(end)
		distance = 0
		if(startPos>endPos):
			temp = startPos
			startPos=endPos
			endPos=temp
		for x in range (startPos,endPos):
			if(distances[row[x]][row[x+1]]>minPower):
				distance = 9999999999999
				break

			distance=distance+distances[row[x]][row[x+1]]


		if(distance<shortestDistance):
			shortestDistance=distance
			shortestPath = row[startPos:endPos+1]

	return shortestPath

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
	#Create complete graph
	matrix = [[0 for x in range(numNodes)] for x in range(numNodes)]
	for col in range(0,numNodes):
		for row in range(0,col+1):
			matrix[row][col]=network[row][col]
	minTree = minimum_spanning_tree(matrix).toarray().astype(int)


	minPower = np.amax(minTree)

	#start and destination array
	transfers = []

	for col in range(0,numNodes):
		for row in range(col+1,numNodes):
			#Finish distance matrix
			matrix[row][col]=network[col][row]

			#Figure out the destinations, and sources of transmissions
			if(network[row][col] != 0):
				if(network[row][col] == 1):
					transfers.append([row, col])
				else:
					transfers.append([col, row])


	#Find path, but using the power calulated in minTree, but normal routing
	noise = []

	#if we can just send directly
	for row in transfers:
		if(matrix[row[0]][row[1]]<=minPower):
			if(row[1] not in noise):
				noise.append(row[1])
			#print 'test'
		else:
			path = GeneratePaths(matrix, minPower, row[0], row[1], numNodes)
			for x in range (1, len(path)):
				if(path[x] not in noise):
					noise.append(path[x])

	#Calculate noise for each receiving node
	for row in transfers:
		noiseDist = []
		for node in noise:
			if(node==row[1]):
				continue
			else:
				noiseDist.append(1/float(matrix[node][row[1]]))
		totalNoise = 1/sum(noiseDist)
		if(totalNoise<1):
			#print "Too loud"
			return -1

	#print "All transmissions sucessful"
	return 1


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
