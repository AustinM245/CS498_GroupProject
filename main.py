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

#Read from the input file to get the JSON files location and the desired
#keypoints for graphing.
def readJSONFile():
    #Open the file
    f = open('Input.txt', 'r')
    # The first line is the file location of the JSON files. The second line is
    # a TRUE/FALSE list for which keypoints the user wants graphed.
    inputs = f.readlines()
    f.close()
    
    #Strip the file location of its trailing newline with strip()
    inputs[0] = inputs[0].rstrip()
    #Split the sequence of true/falses into a seperate list
    inputs[1] = inputs[1].split(",")
    return inputs

 #Loop through all JSON files and 
 def readAllFiles():
    
  
#Reads the string from the JSON file and returns it
def readFromJSON(x,fileLoc):
    x = str(x)
    #Each filename for the JSONS is formatted as follows:
    # 'xxxxxxxxxxxx_keypoints.json'
    #Where the sequence of x's are integers that represent the frame number
    #that the file corresponds to. The input variable x will be the frame number,
    #but it needs to be 12 characters long, with remaining characters being
    #leading zeros. We can use .zfill(12) to add leading zeros that stop at 12
    #total characters
    x = x.zfill(12)
    
    #Can concatenate the file name! Since the long series of 0's increments to
    #represent each file, we can also increment it in a for loop when reading
    #in multiple files
    f = open(fileLoc + '\\' + 'VR1_' + x + '_keypoints.json')
    data = json.load(f)
    f.close()
    return data

def parseData(data):
    
    #Initialize our list of keypoints, this will have 25 lists inside it that
    #represent the 25 keypoints and their 3 values of
    #[x coordinate, y coordinate, confidence level]
    keypoints = []
    
    #The string in the json file is made of many nested lists for differnt
    # keypoint mappings. For now, we're just using the pose_keypoints_2d
    # mapping, so these for loops go into the nested lists to retrieve it
    for people in data['people']:
        for getKeypoints in people['pose_keypoints_2d']:
            keypoints.append(getKeypoints)
            
    #print(keypoints)
    #print('\n')
    
    #After getting the keypoints, they are all in one big list. This command
    # parses the big list into 25 lists each with 3 elements in the following
    # form (as mentioned above)
    #[x coordinate, y coordinate, confidence level]
    keypointsList = [keypoints[x:x+3] for x in range(0, len(keypoints), 3)]
    
    #print(keypointsList)
    
    return keypointsList
