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
	for col in range(0,numNodes-2):
		for row in range(1,NumNodes-1):
			if network[row][col] == 1:
				dummyVariable = 0

				# GEORGE TODO:
				# Add to dict
				# Go through and compare power/noise
				# Return yes/no

def RegularControl(network,numNodes):
	for col in range(0,numNodes-2):
		for row in range(1,NumNodes-1):
			if network[row][col] == 1:
				dummyVariable = 0

				# CHRISTINA TODO:
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
					numNodes = int(line)
					inMatrix = [[0 for x in range(numNodes)] for x in range(numNodes)]
					getNodes = 1
					rowPosition = 0
					continue

				if line == "<end>\n":
					getNodes = 0
					powerResult = PowerControl(inMatrix,numNodes)
					regularResult = RegularControl(inMatrix,numNodes)

					# TODO: ADD OUTPUT TO FILE

					continue

				colPosition = 0
				for value in line.split(","):
					inMatrix[rowPosition][colPosition] = value

if __name__ == '__main__':
    Processor(sys.argv[1:])
