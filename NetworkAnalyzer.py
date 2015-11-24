# # #
# Takes graphs in a file and compiles comparative information on them
#
# Usage: python NetworkAnalyzer.py <filename>
#
# @version 1 - Modified November 24 2015 11:22 AM
# @python-version 2.7
# #

import sys

def powerControl(matrix, outputFile):
	# TODO: Do stuff here to determine whether power control is beneficial for this matrix
	outputFile.write("Power Control Stuff\n")

def processor(inputs):
	try:
		fileName = inputs[0]
	except:
		print("Missing Input.")
		sys.exit(1)

	with open("./" + fileName, "r") as inputFile:
		with open("./" + fileName.split(".")[0] + "_Output.txt", "w") as outputFile:
			
			# Varaibles for the information we want to get for each network 
			# (to make comparisons about what types of networks are better for power control):
			averageDistance = 0
			numberConnections = 0
			numberNodes = 0
			# TODO: change to matrix or move other function into this on
			matrix = 0

			for line in inputFile:
				if line == "<end>\n":
					powerControl(matrix, outputFile)
					averageDistance = averageDistance/2
					numberConnections = numberConnections/2

					try:
						# TODO: This average distance rounds down to whole numbers (dont know if that is desired functionality yet)
						outputFile.write("Average Distance: " + str(averageDistance/numberConnections) + "\n")
						outputFile.write("Number of Connections: " + str(numberConnections) + "\n")
					except:
						outputFile.write("Average Distance: 0\n")
						outputFile.write("Number of Connections: 0\n")

					outputFile.write("Number of Nodes: " + str(numberNodes) + "\n")
					outputFile.write("\n")

					averageDistance = 0
					numberConnections = 0
					numberNodes = 0

					continue

				for node in line.split(","):
					if not int(node) == -1 and not int(node) == 0:
						numberConnections = numberConnections + 1
						averageDistance = averageDistance + int(node)

				numberNodes = numberNodes + 1


if __name__ == '__main__':
    processor(sys.argv[1:])