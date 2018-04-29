import sys
import pandas as pd
import math
import numpy as np
import math
import csv
import nltk
import nltk
from nltk.corpus import stopwords

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

	#stemming for the training set
	ps = nltk.stem.PorterStemmer()
	stop_words = set(stopwords.words('english'))
 	for i in range(0, len(data)):
 		data[i][1] = data[i][1].split() # seperate each word
 		print data[i][1]
 		temp = list()
 		for j in range(1,len(data[i][1])):
 			try:
 				#data[i][1][j] = ps.stem(data[i][1][j])
 				if not data[i][1][j] in stop_words:
 					temp.append(ps.stem(data[i][1][j]))
 				pass
 			except UnicodeDecodeError:
 				print data[i][1][j]
 				pass
 			pass
 		data[i][1] = temp
 		print data[i][1]
 		print
 		pass

	for i in range (0, len(data)):
		#data[i][1] = data[i][1].split() # seperate each word
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
		print data[i]
		prediction = predict(data[i][1], words, countList, totalList)
		bestClass = prediction.index(max(prediction))
		if bestClass != data[i][2]:	
			error += 1

	# print 'ERROR: ', (error*1.0/len(data))
	# print 'Accuracy: ', (1 - (error*1.0/len(data)))
	error =  (error*1.0/len(data))
	accuracy = (1 - error)
	return error, accuracy


def testPredict(data,words, countList, totalList):
	output = pd.DataFrame(index=range(0,len(data)), columns=['id', 'sentiment'])
	for i in range(0, len(data)):
		prediction = predict(data[i][1], words, countList, totalList)
		bestClass = prediction.index(max(prediction))
		output.loc[i, 'id'] = data[i][0]
		output.loc[i, 'sentiment'] = bestClass
	
	output.to_csv('results.csv', index = False)


def predict(dataPoint,words, countList, totalList):
	predict = [1.0] * 5
	#print dataPoint
	for i in range(0, len(dataPoint)): # i is each word
		if dataPoint[i] in words:
			print dataPoint[i]
			if len(dataPoint[i]) <= 2:
				pass
			else :
				# mean = 0*countList[0][dataPoint[i]] + 1*countList[1][dataPoint[i]] + 2*countList[2][dataPoint[i]]
				# mean = mean + 3*countList[3][dataPoint[i]] + 4*countList[4][dataPoint[i]]
				# m2 = 0*countList[0][dataPoint[i]] + 1*countList[1][dataPoint[i]] + 4*countList[2][dataPoint[i]]
				# m2 = mean + 9*countList[3][dataPoint[i]] + 16*countList[4][dataPoint[i]]
				# print "Expected Value: " + str(mean/words[dataPoint[i]])
				# var = (m2/words[dataPoint[i]]) - (mean/words[dataPoint[i]])*(mean/words[dataPoint[i]])
				# print "Varience: " + str(var)

				for j in range (0, len(predict)):
					thisWord = ((1.0*countList[j][dataPoint[i]] + 1)/(totalList[j]+ len(words)))
					print str(j) + ": " + str(thisWord)
					predict[j] = predict[j] + math.log(thisWord)
				

		else:
			for j in range (0, len(predict)):
				predict[j] = predict[j] + math.log(((1.0)/( len(words))))
	
	for x in range (0, len(predict)):
		predict[x] = predict[x] + math.log(totalList[x])
		pass

	print
	return predict

def main():
	trainingFile = sys.argv[1]
	testFile = sys.argv[2]

	data = pd.read_csv(trainingFile, sep=',' , quotechar='"', header=0, engine='python')
	testData = pd.read_csv(testFile, sep=',' , quotechar='"', header=0, engine='python')
	data = data.as_matrix()
	testData = testData.as_matrix()


	out = nbc(data)
	trainReturn = accuracy(data, out[0], out[1], out[2])

	print testData
	print data
	ps = nltk.stem.PorterStemmer()
	#parses into words and stems each word of test set
	for i in range (0, len(testData)):
		testData[i][ 1] = testData[i][1].split()
		for j in range (0, len(testData[i][1])):
			try:
 				testData[i][1][j] = ps.stem(testData[i][1][j])
 				pass
 			except UnicodeDecodeError:
 				testData[i][1][j] = testData[i][1][j]
 				pass
 	print testData
	testPredict(testData, out[0], out[1], out[2])
	print len(out[0])
	print 'ERROR: ', trainReturn[0]
	print 'Accuracy: ', trainReturn[1]
	


if __name__ == '__main__':
  main()
