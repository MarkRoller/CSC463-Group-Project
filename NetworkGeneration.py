# # #
# Takes input to create a number of networks that we can later analyze
#
# Usage: python NetworkGeneration.py (Max Nodes) (Max Distance Between Nodes) (Number Of Networks To Create) (Name Of Output File)
#
# @version 1 - Modified December 8 2015 1:00 PM
# @python-version 2.7
# #

import sys, math
from random import randint

def processor(inputs):
	minNodes = 3
	minDist = 1
	minChance = 25
	maxChance = 75

	try:
		maxNodes = int(inputs[0])
		maxDist = int(inputs[1])
		numNetworks = int(inputs[2])
		outputName = inputs[3]
	except:
		print("Missing Input.")
		sys.exit(1)

	with open("./" + outputName, "w") as outputFile:
		while numNetworks > 0:
			conChance = randint(minChance,maxChance)
			numNodes = randint(minNodes,maxNodes)
			outMatrix = [[0 for x in range(numNodes)] for x in range(numNodes)]
			angleList = [0 for x in range(numNodes)]

			for node in range(0,numNodes):
				angleList[node] = randint(-180,180)

			numConnections = 0
			for row in range(0,numNodes):
				for col in range(row,numNodes):
					if row == col:
						continue

					if row == 0:
						outMatrix[row][col] = randint(minDist,maxDist)
					else:
						b = outMatrix[0][row]
						c = outMatrix[0][col]
						B = angleList[row]
						C = angleList[col]

						if B >= 0:
							if B < C:
								A = angleList[col] - angleList[row]
							else: 
								A = angleList[row] - angleList[col]		
						else:
							if B > C:
								A = ((-1)*angleList[col]) + angleList[row]
							else:
								A = ((-1)*angleList[row]) + angleList[col]

						outMatrix[row][col] = int(math.sqrt(pow(b,2)+pow(c,2)-(2*b*c*(math.cos(A)))))

						if outMatrix[row][col] < 1:
							outMatrix[row][col] = 1

					if randint(0,100) < conChance:
						if randint(0,100) < 50:
							outMatrix[col][row] = 1
						else:
							outMatrix[col][row] = -1
						numConnections = numConnections+1

			if numConnections == 0:
				col = randint(0,numNodes-2)
				row = randint(col+1,numNodes-1)
				outMatrix[row][col] = 1
			
			outputFile.write(str(numNodes)+"\n")
			for row in range(0,numNodes):
				for col in range(0,numNodes):
					outputFile.write(str(outMatrix[row][col]))

					if col == numNodes-1:
						outputFile.write("\n")
					else:
						outputFile.write(",")

			outputFile.write("<end>\n")
			numNetworks = numNetworks-1

if __name__ == '__main__':
    processor(sys.argv[1:])