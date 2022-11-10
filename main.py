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
        filePath = folderName + '/' + letter
        readFromJSON(filePath)
  
#Reads the string from the JSON file and returns it
def readFromJSON(filePath):
    #Get current working directory, add it to file path
    filePath = os.getcwd() + '/' + filePath 
    print(filePath)
    #Get the number of files in the folder so we know how many we need to read
    print(len(os.listdir(filePath)))

    #x = str(x)
    #Each filename for the JSONS is formatted as follows:
    # 'xxxxxxxxxxxx_keypoints.json'
    #Where the sequence of x's are integers that represent the frame number
    #that the file corresponds to. The input variable x will be the frame number,
    #but it needs to be 12 characters long, with remaining characters being
    #leading zeros. We can use .zfill(12) to add leading zeros that stop at 12
    #total characters
    #x = x.zfill(12)
    
    #Can concatenate the file name! Since the long series of 0's increments to
    #represent each file, we can also increment it in a for loop when reading
    #in multiple files
    #f = open(fileLoc + '\\' + 'VR1_' + x + '_keypoints.json')
    #data = json.load(f)
    #f.close()
    #return data
   #parseData(data)

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
    #print('\n')
    
    #After getting the keypoints, they are all in one big list. This command
    # parses the big list into 25 lists each with 3 elements in the following
    # form (as mentioned above)
    #[x coordinate, y coordinate, confidence level]
    keypointsList = [keypoints[x:x+3] for x in range(0, len(keypoints), 3)]
    
    print(keypointsList)
    
    return keypointsList

def main():
    readAllFiles('Jakob_Keypoints')
    
if __name__ == "__main__":
    main()
