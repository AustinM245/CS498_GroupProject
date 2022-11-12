# -*- coding: utf-8 -*-
"""
Created on 

Authors: Austin Morris, Jasmine Parsons, Jakob Clark, Joseph Hurley

Professor: Dr. Eby 

Class: CS498

Purpose: To create a program capable of detecting different letters in American
sign language using machine learning.

Algorithm/Method: Various algorithms will be used. Each team member will implement
a simpelr algorithm while the entire team works together to implement a CNN

BUGS: None known (yet)
                                 
"""
import json
import os 

#Loop through all JSON files and 
def readAllFiles(folderName):
    #Create list to hold data
    keypointDatax = []
    keypointDatay = []
    
    #Loop through the alphabet
    for x in range(0,26):
        #Use ord() to increment the letter for the filepath
        letter = chr(ord('A') + x)
        filePath = folderName + '\\' + letter +'\\'
        allData = readFromJSON(filePath, x)
        keypointDatax = keypointDatax + allData[0]
        keypointDatay = keypointDatay + allData[1]
    keypointData = [keypointDatax, keypointDatay]
    #print(keypointData[0])
    return(keypointData)
  
#Reads the string from the JSON file and returns it
def readFromJSON(filePath, yLabel):
    #Get current working directory, add it to file path
    filePath = os.getcwd() + '\\' + filePath 
    #print(filePath)
    #Get the number of files in the folder so we know how many we need to read
    numFiles = len(os.listdir(filePath))
    #Create a list of y labels that has size of the number of files in the folder
    yData = [yLabel] * numFiles
    #print(yData)
    #Can concatenate the file name! Since the long series of 0's increments to
    #represent each file, we can also increment it in a for loop when reading
    #in multiple files
    
    xData = []
    # Get the file pathnames in each folder and get ALL data from every JSON
    # file. Stuff it all into one big list data[] to be processed later
    for file in os.listdir(filePath):
        f = open(filePath + file)
        temp = json.load(f)
        f.close()
        temp = parseData(temp)
        xData.append(temp)
    allData = [xData, yData]
    return allData

def parseData(data):
    
    #Initialize our list of keypoints, this will have 25 lists inside it that
    #represent the 25 keypoints and their 3 values of
    #[x coordinate, y coordinate, confidence level]
    keypoints = []
    
    #The string in the json file is made of many nested lists for differnt
    # keypoint mappings. For now, we're just using the pose_keypoints_2d
    # mapping, so these for loops go into the nested lists to retrieve it
    for people in data['people']:
        for getKeypoints in people['hand_right_keypoints_2d']:
            keypoints.append(getKeypoints)
    
    #print(keypoints)
    
    #After getting the keypoints, they are all in one big list. This command
    # parses the big list into 25 lists each with 3 elements in the following
    # form (as mentioned above)
    #[x coordinate, y coordinate, confidence level]
    #keypointsList = [keypoints[x:x+3] for x in range(0, len(keypoints), 3)]
    
    return keypoints

#TEMP
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import hinge_loss
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier

#TEMP


def main():
    keypointData = readAllFiles('Jakob_Keypoints')
    
    print(len(keypointData[0]))
    
    for x in range(0,len(keypointData[0])-1):
        if len(keypointData[0][x]) != len(keypointData[0][x+1]):
            print("Problem at: ", x)
    
    
    #print(keypointData[0])
    
    datax_train, datax_test, datay_train, datay_test = train_test_split(keypointData[0], keypointData[1])
    
    #print(datax_train)
    
    #LINEAR CLASSIFIERS
    
    #KNN (ball-tree algorithm)
    KNN = KNeighborsClassifier(n_neighbors = 10, algorithm = 'ball_tree')
    KNN.fit(datax_train,datay_train)
    KNNPredictions1 = KNN.predict(datax_test)
    KNNTestAccuracy1 = accuracy_score(datay_test, KNNPredictions1)
    KNNTrainAccuracy1 = KNN.score(datax_train,datay_train)
    print("KNN (ball-tree algorithm) training set accuracy: %.3f" % KNNTrainAccuracy1)
    print("KNN (ball-tree algorithm) testing set accuracy: %.3f\n" % KNNTestAccuracy1)
    
    #Perceptron
    perc = Perceptron()
    perc.fit(datax_train,datay_train)
    perceptronPredictions = perc.predict(datax_test)
    perceptronTestAccuracy = accuracy_score(datay_test, perceptronPredictions)
    perceptronTrainAccuracy = perc.score(datax_train,datay_train)
    print("Perceptron training set accuracy: %.3f" % perceptronTrainAccuracy)
    print("Perceptron testing set accuracy: %.3f\n" % perceptronTestAccuracy)
    
    #Throws max iteration error. Could be fixed by normalizing data, tuning parameters,
    #or setting max_iter to larger value. 
    #Linear Support Vector machine (hinge loss, l2 regularizer)
    linearSVM = make_pipeline(StandardScaler(),LinearSVC(penalty = 'l2', loss='hinge'))
    linearSVM.fit(datax_train,datay_train)
    linearSVMPredictions = linearSVM.predict(datax_test)
    linearSVMTestAccuracy = accuracy_score(datay_test, linearSVMPredictions)
    linearSVMTrainAccuracy = linearSVM.score(datax_train,datay_train)
    print("Linear SVM training set accuracy (hinge loss, l2 regularizer): %.3f" % linearSVMTrainAccuracy)
    print("Linear SVM testing set accuracy (hinge loss, l2 regularizer): %.3f\n" % linearSVMTestAccuracy)
if __name__ == "__main__":
    main()
