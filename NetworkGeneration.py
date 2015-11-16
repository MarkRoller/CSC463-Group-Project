# # #
# Takes input to create a number of networks that we can later analyze
#
# Usage: python NetworkGeneration.py (Max Nodes) (Max Connections Per Node) (Max Distance Between Connected Nodes) (Number Of Networks To Create) (Name Of Output File)
#
# @version 1 - Modified November 16 2015 12:30 PM
# @python-version 2.7
# #

import sys
from random import randint

def processor(inputs):
	try:
		maxNodes = int(inputs[0])
		maxConn = int(inputs[1])
		maxDist = int(inputs[2])
		numNetworks = int(inputs[3])
		outputName = inputs[4]
	except:
		print("Missing Input.")
		sys.exit(1)

	with open("./" + outputName, "w") as outputFile:
		while numNetworks > 0:
			
			outNodes = randint(1,maxNodes)
			outMatrix = [[-1 for x in range(outNodes)] for x in range(outNodes)]
			numNodes = outNodes

			while outNodes > 0:
				outConnections = randint(1,maxConn)
				rowCounter = 0

				while outConnections > 0:
					connection = randint(1,numNodes)

					if outMatrix[outNodes-1][connection-1] == -1:
						if outNodes == connection:
							outMatrix[outNodes-1][connection-1] = 0
							outMatrix[connection-1][outNodes-1] = 0
						else:
							outTemp = randint(1,maxDist)
							outMatrix[outNodes-1][connection-1] = outTemp
							outMatrix[connection-1][outNodes-1] = outTemp

						outConnections = outConnections-1
					else:
						rowCounter = rowCounter+1

					if rowCounter == numNodes*2:
						break
				
				outNodes = outNodes-1
			
			tempNodes = numNodes
			while tempNodes > 0:
				temp2Nodes = numNodes
				while temp2Nodes > 0:
					outputFile.write(str(outMatrix[tempNodes-1][temp2Nodes-1]))
					temp2Nodes = temp2Nodes-1

					if temp2Nodes == 0:
						outputFile.write("\n")
					else:
						outputFile.write(",")

				tempNodes = tempNodes-1

			outputFile.write("\n\n")
			numNetworks = numNetworks-1

if __name__ == '__main__':
    processor(sys.argv[1:])