# -*- coding: utf-8 -*-
"""
Created on 

Authors: 

Student ID: 

Professors: 

Class: 

Purpose:

Algorithm/Method: 

BUGS: 
                                 
"""
import json
import os 

#Loop through all JSON files and 
def readAllFiles(folderName):
    #Create list to hold data
    keypointData = []
    
    #Loop through the alphabet
    for x in range(0,26):
        #Use ord() to increment the letter for the filepath
        letter = chr(ord('A') + x)
        filePath = folderName + '\\' + letter +'\\'
        allData = readFromJSON(filePath, x)
        keypointData.append(allData)
    print(keypointData)
  
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
    
    #After getting the keypoints, they are all in one big list. This command
    # parses the big list into 25 lists each with 3 elements in the following
    # form (as mentioned above)
    #[x coordinate, y coordinate, confidence level]
    keypointsList = [keypoints[x:x+3] for x in range(0, len(keypoints), 3)]
    
    return keypointsList

def main():
    readAllFiles('Jakob_Keypoints')
    
if __name__ == "__main__":
    main()
