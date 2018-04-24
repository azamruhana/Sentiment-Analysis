import sys
import pandas as pd
import math
import numpy as np
import math

def printDict(count):
	for i in range(0, len(count)):
		print count[i]

def nbc(data):
	pass

def zeroOneAcc(data, countZero, countOne, count, cZero, cOne):
	error = 0
	for i in range(0, len(data)):
		prediction = predict(data[i], countZero, countOne, count, cZero, cOne)
		if prediction[0] != data[i][14]:
			error = error + 1
	#print "ERROR: " + str((error * 1.0)/len(data))
	return (error * 1.0)/len(data)

def main():
	trainingFile = sys.argv[1]
	testFile = sys.argv[2]

	data = pd.read_csv(trainingFile, sep=',' , quotechar='"', header=0, engine='python')
	testData = pd.read_csv(testFile, sep=',' , quotechar='"', header=0, engine='python')

	#np.random.shuffle(data)
	data = data.as_matrix()
	testData = testData.as_matrix()



if __name__ == '__main__':
  main()
