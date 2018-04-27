import sys
import pandas as pd
import math
import numpy as np
import math
import csv

def printDict(count):
	for i in range(0, len(count)):
		print "COUNT NUM: " + str(i)
		print count[i]
		print

def nbc(data):
	#make dictionaries
	words = dict() #count total of each word
	countList = [dict(), dict(), dict(), dict(), dict()]
	totalList = [0]*5

	for i in range (0, len(data)):
		data[i][1] = data[i][1].split() # seperate each word
		for j in range (0, len(data[i][1])): #insert each word from one data set
			if data[i][1][j] not in words:
				words[data[i][1][j]] = 0
				for x in range (0,len(countList)):
					countList[x][data[i][1][j]] = 0

	for i in range (0, len(data)): # counting
		out = data[i][2]
		for j in range(0, len(data[i][1])): # loop through each word
			countList[out][data[i][1][j]]+= 1
			words[data[i][1][j]] += 1
			totalList[out] += 1
			
	return words, countList, totalList
	

def zeroOneAcc(data, countZero, countOne, count, cZero, cOne):
	error = 0
	for i in range(0, len(data)):
		prediction = predict(data[i], countZero, countOne, count, cZero, cOne)
		if prediction[0] != data[i][14]:
			error = error + 1
	#print "ERROR: " + str((error * 1.0)/len(data))
	return (error * 1.0)/len(data)

def accuracy(data,words, countList, totalList):
	error = 0
	for i in range(0, len(data)):
		prediction = predict(data[i][1], words, countList, totalList)
		bestClass = prediction.index(max(prediction))
		if bestClass != data[i][2]:	
			error += 1

	print 'ERROR: ', (error*1.0/len(data))
	print 'Accuracy: ', (1 - (error*1.0/len(data)))

def testPredict(data,words, countList, totalList):
	output = pd.DataFrame(index=range(0,len(data)), columns=['id', 'sentiment'])
	for i in range(0, len(data)):
		prediction = predict(data[i][1], words, countList, totalList)
		bestClass = prediction.index(max(prediction))
		output.loc[i, 'id'] = data[i][0]
		output.loc[i, 'sentiment'] = bestClass
	print output
	print
	print len(output)
	output.to_csv('results.csv', index = False)


def predict(dataPoint,words, countList, totalList):
	predict = [1.0] * 5

	for i in range(0, len(dataPoint)): # i is each word
		if dataPoint[i] in words:
			for j in range (0, len(predict)):
				predict[j] = predict[j] * ((1.0*countList[j][dataPoint[i]] + 1)/(words[dataPoint[i]]+ len(words)))
		else:
			for j in range (0, len(predict)):
				predict[j] = predict[j] * ((1.0)/len(words))
	return predict

def main():
	trainingFile = sys.argv[1]
	testFile = sys.argv[2]

	data = pd.read_csv(trainingFile, sep=',' , quotechar='"', header=0, engine='python')
	testData = pd.read_csv(testFile, sep=',' , quotechar='"', header=0, engine='python')
	data = data.as_matrix()
	testData = testData.as_matrix()

	out = nbc(data)
	accuracy(data, out[0], out[1], out[2])

	for i in range (0, len(testData)):
		testData[i][1] = testData[i][1].split()
	testPredict(testData, out[0], out[1], out[2])
	


if __name__ == '__main__':
  main()
