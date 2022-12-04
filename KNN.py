# -*- coding: utf-8 -*-
"""

"""

#Importing Fucntions

from math import sqrt
from random import shuffle

#Calculate the Euclidain distance
def calculateDistance(row1, row2):
    return sqrt(sum([(row1[0][i] - row2[0][i])**2 for i in range(len(row1[0]))]))

#Compute the distances between the test data row and the rest of the rows in the dataset
def getNearestNeighbors(dataset, testDataRow, numNeighbors):
    distances = [(currDataRow, calculateDistance(testDataRow, currDataRow)) 
                 for currDataRow in dataset]
    
    #print(distances)
    #Sort the distances in ascending order. Since "distances" has two elements, 
    #use lambda to define this and sort properly.
    distances.sort(key=lambda x: x[1])
    #print(distances)
    
    # Get the top k neighbors, defined by numNeighbors
    #NOTE: Changed this to i+1 since otherwise the test row would detect itself
    #as the nearest neighbor! Now the program no longer detects itself as
    #the true nearest neighbor
    topNeighbors = [distances[i+1][0] for i in range(numNeighbors)]
    #print("\nTHE TOP NEIGHBORS:", topNeighbors)
    return topNeighbors

# Predict the label of the test data by finding the most frequent label in all 
# the nearest neighbors
def predictLabel(dataset, testDataRow, numNeighbors):
    
    # Get top-k neighbors
    topNeighbors = getNearestNeighbors(dataset, testDataRow, numNeighbors)
    
    # Get most frequent label
    output_values = [row[-1] for row in topNeighbors] #Gets last element in list (the label)
    #print(output_values)
    prediction = max(set(output_values), key=output_values.count)
    
    return prediction

#Run the custom KNN algorithm
def run_KNN(keypointData):
    #Parse teh data a little more, to make the algorithm a little easier.
    #Now instead of being in the form
    #[ [ [ first set of 40 x-y coords for each keypoint ] ... [ ~300th set of 40 x-y coords ] ]
    # [label (0-25) for each set] ]
    #NOTE: each set of 40 x-y coords represents a frame in a video
    #NOTE: each label represents a letter a-z, or 0-25
    
    #It will be in the form
    #[ [ [ first set of 40 x-y coords ], label ], ...,
    #[ [ ~300th set of 40 x-ycoords ], label] ]
    #This way, it simplifies the manner in which you can retrieve a label for a
    #frame in future functions. This also simplifies shuffling the data
    parsedData = []
    for row in range(len(keypointData[0])):
        parsedData.append([keypointData[0][row], keypointData[1][row]])
    
    #print("KNN module working!")
    
    #shuffle the data
    shuffle(parsedData)
    
    # Found throught validating the data in testing (should be an odd number!)
    numNeighbors = 5
    
    #testDataRow = parsedData[8300]
    
    predictedLabels = []
    
    #for row in range(len(parsedData)):
    for row in range(100):
        predictedLabels.append(predictLabel(parsedData, parsedData[row], numNeighbors))
        
    #print(predictedLabels)
    
    numCorrectPredictions = 0
    for label in range(len(predictedLabels)):
        if predictedLabels[label] == parsedData[label][1]:
            numCorrectPredictions += 1
            
    accuracy = numCorrectPredictions / len(predictedLabels)
    
    print("Average accuracy score for custom KNN algorithm: %.3f\n" % accuracy)
        
    
    
    
    
    