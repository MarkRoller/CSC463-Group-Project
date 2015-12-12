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

def GeneratePaths(distances, minPower, start, end, numNodes):
	matrix = [x for x in range(numNodes)]

	allPossiblePaths = []
	allPossiblePaths.append(itertools.permutations(matrix))
	allPossiblePaths = list(itertools.permutations(matrix, len(matrix)))
	shortestDistance = 9999999999999
	shortestPath = []

	for row in allPossiblePaths:
		startPos = row.index(start)
		endPos = row.index(end)
		distance = 0

		if startPos > endPos:
			temp = startPos
			startPos = endPos
			endPos = temp

		for x in range(startPos,endPos):
			if distances[row[x]][row[x+1]] > minPower:
				distance = 9999999999999
				break

			distance = distance + distances[row[x]][row[x+1]]

		if distance < shortestDistance:
			shortestDistance = distance
			shortestPath = row[startPos:endPos+1]

	return shortestPath

def RegularControl(network,numNodes):
	matrix = [[0 for x in range(numNodes)] for x in range(numNodes)]

	for col in range(0,numNodes):
		for row in range(0,col+1):
			matrix[row][col] = network[row][col]

	minTree = minimum_spanning_tree(matrix).toarray().astype(int)
	minPower = np.amax(minTree)
	transfers = []

	for col in range(0,numNodes):
		for row in range(col+1, numNodes):
			matrix[row][col] = network[col][row]

			if network[row][col] != 0:
				if network[row][col] == 1:
					transfers.append([row, col])
				else:
					transfers.append([col, row])

	noise = []
	for row in transfers:
		if matrix[row[0]][row[1]] <= minPower:
			if row[1] not in noise:
				noise.append(row[1])
		else:
			path = GeneratePaths(matrix, minPower, row[0], row[1], numNodes)
			for x in range (1, len(path)):
				if path[x] not in noise:
					noise.append(path[x])

	for row in transfers:
		noiseDist = []
		for node in noise:
			if node == row[1]:
				continue
			else:
				noiseDist.append(1/float(matrix[node][row[1]]))

		totalNoise = 1/sum(noiseDist)

		if totalNoise < 1:
			return -1

	return 1

def PowerControl(network,numNodes):
	network_fail = 0
	nodePower = {}

	for row in range(0,numNodes):
		nodePower[row] = 0

	for row in range(1,numNodes):
		for col in range(0,row):
			if network[row][col] == 1:
				if network[col][row] > nodePower[row]:
					nodePower[row] = network[col][row]

			if network[row][col] == -1:
				if network[col][row] > nodePower[col]:
					nodePower[col] = network[col][row]
				
	for entry in nodePower:
		receiving = []

		if nodePower[entry] == 0:
			continue
		else:
			for row in range(1,numNodes):	
				if network[row][entry] == -1:
					receiving.append(row)
			for col in range(0,entry):
				if network[entry][col] == 1:
					receiving.append(col)
		
		for y in receiving:
			nodesReached = []
			pTop = 0
			pBottom = 0

			for x in nodePower:
				if nodePower[x] == 0 or x == y:
					continue
				if network[x][y] <= nodePower[x]:
					nodesReached.append(x)	
					
			for node in nodesReached:
				if node > y:
					if network[node][y] == -1:
						pTop = pTop + (float(nodePower[node]) / float(network[y][node]))
					else:
						pBottom = pBottom + (float(nodePower[node]) / float(network[y][node]))	
				else:
					if network[y][node] == -1:
						pTop = pTop + (float(nodePower[node]) / float(network[node][y]))
					else:
						pBottom = pBottom + (float(nodePower[node]) / float(network[node][y]))					
	
			if pTop > 0 and pBottom == 0:
				continue
			if (pTop / pBottom) < 1:
				network_fail = 1
	
	if network_fail == 1:
		return -1
	else:	
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
					numNodes = int(line.split("\n")[0].split(",")[0])
					averageDistance = int(line.split("\n")[0].split(",")[1])
					inMatrix = [[0 for x in range(numNodes)] for x in range(numNodes)]
					getNodes = 1
					rowPosition = 0
					continue

				if line.split("\n")[0] == "<end>":
					getNodes = 0
					powerResult = PowerControl(inMatrix,numNodes)
					regularResult = RegularControl(inMatrix,numNodes)

					outputFile.write("Number of Nodes - " + str(numNodes) + "\n")
					outputFile.write("Average Distance - " + str(averageDistance) + "\n\n")

					if powerResult == -1:
						outputFile.write("Power Control Result - Failed\n")
					else:
						outputFile.write("Power Control Result - Passed\n")
					
					if regularResult == -1:
						outputFile.write("Regular Result - Failed\n")
					else:
						outputFile.write("Regular Result - Passed\n")

					outputFile.write("\n--------------------\n\n")
					continue

				colPosition = 0
				for value in line.split("\n")[0].split(","):
					inMatrix[rowPosition][colPosition] = int(value)
					colPosition = colPosition+1
				rowPosition = rowPosition+1

if __name__ == '__main__':
    Processor(sys.argv[1:])
