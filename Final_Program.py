# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 04:18:52 2022, for the spring semester

Author: Austin Morris

Student ID: 2596

Professors: Dr. Jaromczyk and Dr. Lefebvre

Class: CS 395 Independent Research

Purpose: To create a prototype that obtains and visualizes the data from JSON
files that contain keypoints from individual bodyparts in OpenPose. This data
will serve as the basis for a future program which analyzes it to determine the
differences of nonverbal movement between VR and reality

Algorithm/Method: The information in the JSON files is contained in nested lists,
so much string manipulation was used to get them into a readable format. Each
file represnts a frame that contains 25 keypoints of individual body parts, and
each keypoint contains 3 data points, the x coordinate, y coordinate, and a
confidence level. So, this program will output (number of files) * 25 * 3 data 
points. The outputted format for 10 frame will look like this:
    [ frame1[ keypoint1[x coordinate, y-coordinate, confidence ], ... 
             keypoint25[ x, y, conf. ] ], ... frame10[ keypoint1[ x, y, conf. ],
             ... keypoint25[ x, y, conf. ] ] ]

Compilation: The user only needs to input the file pathname of the location of
the JSON files. In this prototype, the folders that contain JSON files are:
    Moving_Right_Hand
    Moving_Left_Hand
    Moving_Both_Hands

BUGS: There are still some (0,0) outliers that manage to get through the code and into
graphs. Not a huge deal, but still something to get rid of in the future.
                                 
"""

import json
import matplotlib.pyplot as plt
import numpy as np

#Read from the input file to get the JSON files location and the desired
#keypoints for graphing.
def readFromInput():
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

# This function graphs the data of frameList by taking the x-coordinates and
# y-coordinates from the list and making them into 2 seperate lists to plot.
# The plot will give us an idea of the amount of movement certain keypoints
# made over time.
def graph(frameList, inputs):
    # Get the number of frames and the number of keypoints per frame
    numFrames = len(frameList)
    numKeypoints = len(frameList[0])
    
    xList = []
    currxList = []
    yList = []
    curryList =[]
    
    # This for loop will organize our data into two lists, xList and yList.
    # xList will have the x-coordinates arranged into a nested list as shown:
    #   [ frame1[x0,x1,x2,...,x24], frame2[x0,x1,x2,...,x24], ... framex[...] ]
    # where x0,x1,x2,... are represntative of their keypoints. So, for example,
    # x0 represents the x-coordinate of the nose keypoint. yList is organized
    # in the same way.
    for frame in range(0, numFrames):
        # By the time this for loop has finished, currxList will have the
        # x-coordinates of the keypoints in one frame.
        for keypoint in range(0, numKeypoints):
            #print(keypoint)
            currxList.append(frameList[frame][keypoint][0])
            curryList.append(frameList[frame][keypoint][1])
        xList.append(currxList)
        yList.append(curryList)
        
        #Reset the currxList and curryList variables
        currxList = []
        curryList = []
        
    #xList[0][1] = 1000.0 - xList[0][1]
    #print("THIS IS XLIST:")
    #print(xList)
    #print("THIS IS YLIST:")
    #print(yList)
    
    # The x-y coordinates are on a scale from 0-1000 and OpenPose inverts them
    # in the JSON files (up is down, right is left), so uninvert them.
    
    
    for frame in range(0, numFrames):
        for keypoint in range(0, numKeypoints):
            if (xList[frame][keypoint] != 0.0):
                xList[frame][keypoint] = 1500.0 - xList[frame][keypoint]
            if (yList[frame][keypoint] != 0.0):
                yList[frame][keypoint] = 1000.0 - yList[frame][keypoint]
    """
    frameCount = 0
    while frameCount < numFrames:
        for keypoint in range(0, numKeypoints):
            if (xList[frameCount][keypoint] != 0.0):
                xList[frameCount][keypoint] = 1500.0 - xList[frameCount][keypoint]
            if (yList[frameCount][keypoint] != 0.0):
                yList[frameCount][keypoint] = 1000.0 - yList[frameCount][keypoint]
            
            print('frameCount: ' + str(frameCount))
            # If the x or y coordinate is an outlier, remove the frame.
            if ( (xList[frameCount][keypoint] < 50.0 or xList[frameCount][keypoint] > 950.0)
                or (yList[frameCount][keypoint] < 50.0 or yList[frameCount][keypoint] > 950.0)):
                del xList[frameCount]
                del yList[frameCount]
                numFrames = numFrames - 1
                break
            
            frameCount = frameCount + 1
    """        
    
    # Now our x and y coordinates are organized into their own lists. However,
    # we have to manipulate our lists into non-nested lists if we wish to plot!
    #print(xList)
    #print(yList)
    
    #For the prototype, I made the plot only for three keypoints. However,
    # in the future, we can slightly edit the code to plot as many keypoints as
    # we want, or even ask for user input on the specific keypoints they want
    # plotted.
    
    #These are the names for each keypoint (i.e. keypoint 0 is the nose) 
    keypointNames = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
                     "LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle",
                     "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar",
                     "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe",
                     "RHeel",]
    
    # These nested lists will hold the x-y coordinates per frame for each keypoint.
    # xKeypoints[0][2] will hold the x coordinate of the nose in the third frame.
    xKeypoints = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
                  [],[],[],[],[]]
    yKeypoints = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
                  [],[],[],[],[]]
    
    # This loop will create the x-y lists for each keypoint. These lists can be
    # used with the plot function to create our plot! 
    for frame in range(0, numFrames):
        for keypoint in range(0, numKeypoints):
            if (inputs[keypoint]):
                xKeypoints[keypoint].append(xList[frame][keypoint])
                yKeypoints[keypoint].append(yList[frame][keypoint])
    
    # Print the total number of head turns made (left and right). To determine
    # this we will use the left ear (17) and right ear (18) keypoints.
    headMovement(numFrames, xKeypoints[17], yKeypoints[17], xKeypoints[18],
                 yKeypoints[18])
    
    #Print the chest movement (shifting from left to right)
    chestMovement(numFrames, xKeypoints[1], yKeypoints[1], xKeypoints[2], 
                  yKeypoints[2], xKeypoints[5], yKeypoints[5])
    
    # After the x-y coordinates have been organized into their respective lists,
    # we can plot them. But only plot the keypoints requested by the user in
    # the input file!
    for keypoint in range(0, numKeypoints):
        if (inputs[keypoint] == 'TRUE'):
            # Give an idea of the amount of movement the keypoint did
            #movementEstimate(numFrames, keypointNames[keypoint],
            #                 xKeypoints[keypoint], yKeypoints[keypoint])
            
            
            xKeypoints[keypoint][ xKeypoints==0 ] = np.nan
            yKeypoints[keypoint][ yKeypoints==0 ] = np.nan
            
            plt.scatter(xKeypoints[keypoint], yKeypoints[keypoint],
                        label = keypointNames[keypoint])

    # Name the axes
    plt.xlabel("X-Coordinate")
    plt.ylabel("Y-Coorindate")
    
    # Title the graph
    plt.title("Positon in Space of Keypoints")
    
    # Show a legend
    plt.legend()
    
    # Show the graph
    plt.show()
    
# Give a rough idea on the amount of movement a certain keypoint made
# over the video.
def movementEstimate(numFrames, keypointName, xKeypoints, yKeypoints):
    xsum = 0
    ysum = 0
    for frame in range(0, numFrames-1):
        xsum = xsum + abs(xKeypoints[frame]-xKeypoints[frame+1])
        ysum = ysum + abs(yKeypoints[frame]-yKeypoints[frame+1])
    totalsum = xsum + ysum
    print("The total \"movement\" for " + keypointName + " is: " + str(totalsum))
    
    
def chestMovement(numFrames, xKeypointsChest, yKeypointsChest, xKeypointsRShoulder,
                  yKeypointsRShoulder, xKeypointsLShoulder, yKeypointsLShoulder):
    # the students always begin staring straight at the camera
    isLeft = False
    isRight = False
    #isCentered = True
    
    timeOnLeft = []
    timeOnRight = []
    timeCentered = []
    
    # Originally, the starting frame of the chest was used as the "anchor point,"
    # where any movement left or right of that specific point would be considered
    # as "left" or "right" movement. However, some students started in odd positions,
    # like leaning to the left, which threw off the whole algorithm. Instead,
    # I am using the average x-coordinate of the chest through all frames. This
    # way we can still identify trends in the data without worrying about the
    # starting point of the student.
    
    averageCenter = sum(xKeypointsChest) / len(xKeypointsChest)
    
    # You are considered to be left or right of the average center when you are
    # 1/2 a shoulder width away from it.
    centerThreshold = round(abs(xKeypointsLShoulder[0] - xKeypointsChest[0]), 2)
    centerUpperThreshold = averageCenter + (centerThreshold/2.0) # Beyond upper = right
    centerLowerThreshold = averageCenter - (centerThreshold/2.0) # Below lower = left
    frameCount = 1
    timer = 0
    centTimer = 0

    # Loop through all frames to detect where the person is in/out of the center
    while frameCount < numFrames:
        centFlag = True
        if (xKeypointsChest[frameCount] > centerUpperThreshold) and (isRight):
            centFlag = False
            timer = timer + 1
            
        elif (xKeypointsChest[frameCount] > centerUpperThreshold) and (isRight == False):
            centFlag = False
            isRight = True
            timer = timer + 1
            
        elif (xKeypointsChest[frameCount] < centerUpperThreshold) and (isRight):
            centFlag = False
            isRight = False
            timeOnRight.append(timer)
            # Timer is 1 instead of 0 because the person has been centered for 1 frame now.
            timer = 1
        elif (xKeypointsChest[frameCount] < centerLowerThreshold) and (isLeft):
            centFlag = False
            timer = timer + 1
            
        elif (xKeypointsChest[frameCount] < centerLowerThreshold) and (isLeft == False):
            centFlag = False
            isLeft = True
            timer = timer + 1
            
        elif (xKeypointsChest[frameCount] > centerLowerThreshold) and (isLeft):
            centFlag = False
            isLeft = False
            timeOnLeft.append(timer)
            timer = 1   
        #else: Do nothing
        if (centFlag):
            centTimer = centTimer + 1
        elif (centFlag == False) and (centTimer != 0):
            timeCentered.append(centTimer)
            centTimer = 0
            
        frameCount = frameCount + 1
        
    
    # Convert lists from frames into seconds for future use
    timeOnLeftSec = [x / 30.0 for x in timeOnLeft]
    timeOnRightSec = [x / 30.0 for x in timeOnRight]
    timeCenteredSec = [x / 30.0 for x in timeCentered]
    
    totalTimeLeft = sum(timeOnLeft)
    totalTimeLeftSec = round(totalTimeLeft / 30.0, 2)
    
    totalTimeCentered = sum(timeCentered)
    totalTimeCenteredSec = round(totalTimeCentered / 30.0, 2)
    
    totalTimeRight = sum(timeOnRight)
    totalTimeRightSec = round(totalTimeRight / 30.0, 2)
    
    ratioTimeLeft = round(totalTimeLeft / numFrames, 2)
    ratioTimeRight = round(totalTimeRight / numFrames, 2)
    ratioTimeCentered = 1.00 - ratioTimeLeft - ratioTimeRight
    
    averageLeftLength = round(sum(timeOnLeftSec) / len(timeOnLeftSec), 2)
    averageRightLength = round(sum(timeOnRightSec) / len(timeOnRightSec), 2)
    averageCenteredLength = round(sum(timeCenteredSec) / len(timeCenteredSec), 2)
    
    maxLeftTurnLength = round(max(timeOnLeftSec),2)
    maxRightTurnLength = round(max( timeOnRightSec),2)
    maxCenteredLength = round(max(timeCenteredSec),2)
    
    minLeftTurnLength = round(min(timeOnLeftSec),2)
    minRightTurnLength = round(min( timeOnRightSec),2)
    minCenteredLength = round(min(timeCenteredSec),2)
    
    #Print functions are ordered according to the Excel sheet for convenience
    print("\nRatio of time shifted left: ", str(ratioTimeLeft))
    print("Ratio of time centered: ", str(ratioTimeCentered))
    print("Ratio of time shifted right: ", str(ratioTimeRight))
    
    if xKeypointsChest[0] > centerUpperThreshold:
        startPosition = "to the right"
    elif xKeypointsChest[0] < centerLowerThreshold:
        startPosition = "to the left"
    else:
        startPosition = "centered"
    print("Do they start to the left, centered, or to the right: " + startPosition)
    
    print("Total time spent shifted left (seconds): ", str(totalTimeLeftSec))
    print("Average length of left shifts (seconds): ", str(averageLeftLength))
    print("Longest left shift (seconds): ", str(maxLeftTurnLength))
    print("Shortest left shift (seconds): ", str(minLeftTurnLength))
    print("Total time spent centered (seconds): ", str(totalTimeCenteredSec))
    print("Average length of time centered (seconds): ", str(averageCenteredLength))
    print("Longest time centered (seconds): ", str(maxCenteredLength))
    print("Shortest time centered (seconds): ", str(minCenteredLength))
    print("Total time spent shifted right (seconds): ", str(totalTimeRightSec))
    print("Average length of right shifts (seconds): ", str(averageRightLength))
    print("Longest right shift (seconds): ", str(maxRightTurnLength))
    print("Shortest right shift (seconds): ", str(minRightTurnLength))
    
    
def headMovement(numFrames, xKeypointsLeftEar, yKeypointsLeftEar,
                 xKeypointsRightEar, yKeypointsRightEar):
    
    # The students always begin staring straight at the camera
    isTurnedLeft = False
    isTurnedRight = False
    
    numHeadTurnsLeft = 0
    numHeadTurnsRight = 0
    # The FPS (frame per second) the videos are recorded in is about 30 FPS.
    # For example, 150 frames is about 5 seconds.
    
    
    
    frameCount = 0
    # Based on experimental observation, we can assume that multiple, non-consecutive
    # tacking losses on an ear are part of the same head turn. A countdown of
    # 10 frames (about 1/3 of a second) is used to determine if the detected
    # head turn is part of the same previous turn.
    countdown = 10
    
    # The exact length in seconds of a head turn is approximated. The actual
    # time can be up to 1/3 of a second (10 frames) less due to the complexity
    # of the algorithm.
    timer = 0
    turnTimeLengthLeft = []
    
    centTimer = 0
    timeLengthCent = []
    
    turnTimeLengthRight = []
    while frameCount < numFrames:
        centFlag = True
        if ((xKeypointsLeftEar[frameCount] == 0) and (isTurnedLeft == False)):
            centFlag = False
            countdown = 10
            numHeadTurnsLeft = numHeadTurnsLeft + 1
            isTurnedLeft = True
            timer = timer + 1
        elif ((xKeypointsLeftEar[frameCount] != 0) and (isTurnedLeft == True)):
            centFlag = False
            countdown = countdown - 1
            timer = timer + 1
            if countdown == 0:
                isTurnedLeft = False
                countdown = 10
                #handle timer
                turnTimeLengthLeft.append(timer)
                timer = 0
        elif ((xKeypointsLeftEar[frameCount] == 0) and (isTurnedLeft == True)):
            centFlag = False
            countdown = 10
            timer = timer + 1
        elif ((xKeypointsRightEar[frameCount] == 0) and (isTurnedRight == False)):
            centFlag = False
            countdown = 10
            numHeadTurnsRight = numHeadTurnsRight + 1
            isTurnedRight = True
            timer = timer + 1
        elif ((xKeypointsRightEar[frameCount] != 0) and (isTurnedRight == True)):
            centFlag = False
            countdown = countdown - 1
            timer = timer + 1
            if countdown == 0:
                isTurnedRight = False
                countdown = 10
                #handle timer
                turnTimeLengthRight.append(timer)
                timer = 0
        elif ((xKeypointsRightEar[frameCount] == 0) and (isTurnedRight == True)):
            centFlag = False
            countdown = 10
            timer  = timer + 1
        #else: do nothing
        if centFlag: # Then the head is centered
            centTimer = centTimer + 1
        elif ((centFlag == False) and (centTimer != 0)):
            timeLengthCent.append(centTimer)
            centTimer = 0
         
                
        frameCount = frameCount + 1
    
    # Convert lists from frames into seconds for future use
    turnTimeLengthSecLeft = [x / 30.0 for x in turnTimeLengthLeft]
    turnTimeLengthSecRight = [x / 30.0 for x in turnTimeLengthRight]
    centeredTimeLengthSec = [x / 30.0 for x in timeLengthCent]
    
    totalTurnTimeLeft = sum(turnTimeLengthLeft)
    totalTurnTimeSecLeft = round(totalTurnTimeLeft / 30.0, 2)
    
    totalTimeCentered = sum(timeLengthCent)
    totalTimeSecCentered = round(totalTimeCentered / 30.0, 2)
    
    totalTurnTimeRight = sum(turnTimeLengthRight)
    totalTurnTimeSecRight = round(totalTurnTimeRight / 30.0, 2)
    
    ratioTimeTurnedLeft = round(totalTurnTimeLeft / numFrames, 2)
    ratioTimeTurnedRight = round(totalTurnTimeRight / numFrames, 2)
    ratioTimeCentered = 1.00 - ratioTimeTurnedLeft - ratioTimeTurnedRight
    
    totalNumTurns = numHeadTurnsLeft + numHeadTurnsRight
    
    averageLeftTurnLength = round(sum(turnTimeLengthSecLeft) / len(turnTimeLengthSecLeft), 2)
    averageRightTurnLength = round(sum(turnTimeLengthSecRight) / len(turnTimeLengthSecRight), 2)
    averageCenteredLength = round(sum(centeredTimeLengthSec) / len(centeredTimeLengthSec), 2)
    
    maxLeftTurnLength = round(max(turnTimeLengthSecLeft),2)
    maxRightTurnLength = round(max(turnTimeLengthSecRight),2)
    maxCenteredLength = round(max(centeredTimeLengthSec),2)
    
    minLeftTurnLength = round(min(turnTimeLengthSecLeft),2)
    minRightTurnLength = round(min(turnTimeLengthSecRight),2)
    minCenteredLength = round(min(centeredTimeLengthSec),2)
    
    #Print functions are ordered according to the Excel sheet for convenience
    print("Ratio of time turned left: ", str(ratioTimeTurnedLeft))
    print("Ratio of time turned right: ", str(ratioTimeTurnedRight))
    print("Ratio of time centered: ", str(ratioTimeCentered))
    print("Total number of turns: ", str(totalNumTurns))
    print("Total time spent with head turned to the left (seconds): ", str(totalTurnTimeSecLeft))
    print("Average length of left head turns (seconds): ", str(averageLeftTurnLength))
    print("Longest left head turn (seconds): ", str(maxLeftTurnLength))
    print("Shortest left head turn (seconds): ", str(minLeftTurnLength))
    print("Total time spent with head turned to the right (seconds): ", str(totalTurnTimeSecRight))
    print("Average length of right head turns (seconds): ", str(averageRightTurnLength))
    print("Longest right head turn (seconds): ", str(maxRightTurnLength))
    print("Shortest right head turn (seconds): ", str(minRightTurnLength))
    print("Total time spent with head centered (seconds): ", str(totalTimeSecCentered))
    print("Average length of time head was centered (seconds): ", str(averageCenteredLength))
    print("Longest time head was centered (seconds): ", str(maxCenteredLength))
    print("Shortest time head was centered (seconds): ", str(minCenteredLength))
    
def main():
    
    """
    # The first line is the file location of the JSON files. The second line is
    # a TRUE/FALSE list for which keypoints the user wants graphed.
    inputs = readFromInput()
    #Make a list that store the data for each frame
    frameList = []
    
    #First, read from x JSON files. Ideally, this will be changed to read y
    #files, where y is a number from user input, or perhaps the total number
    #of JSON files in OpenPose's output folder
    for x in range(0, 5000):
        data = readFromJSON(x, inputs[0])
        #Parse the data into 25 lists of 3 elements (the keypoints)
        keypointsList = parseData(data)
        #Append this data to the frame list
        frameList.append(keypointsList)
    
    #The information here is messy to read, but as data it is quite orderly.
    #There are 3 layers of lists. The first list is made up of 30 frames.
    #Each frame is a list of 25 keypoints. And each keypoint is a list of
    #3 data points (x,y-coordinates and confidence level). For each frame we
    #analyze the amount of work and data to store will increase linearly. Every
    #frame has 75 data points to store, so in this example we have 30*75= 2250
    #data points.
    #print(frameList)
    
    # Now graph this data into a visual format. For this protoype, we will
    # only graph 3 keypoints, the nose, left hand, and right hand.
    graph(frameList, inputs[1])
    
    frameList = []
    
    for x in range(5000, 10000):
        data = readFromJSON(x, inputs[0])
        #Parse the data into 25 lists of 3 elements (the keypoints)
        keypointsList = parseData(data)
        #Append this data to the frame list
        frameList.append(keypointsList)
    
    graph(frameList, inputs[1])
    
    frameList = []
        
    for x in range(10000, 14100):
        data = readFromJSON(x, inputs[0])
        #Parse the data into 25 lists of 3 elements (the keypoints)
        keypointsList = parseData(data)
        #Append this data to the frame list
        frameList.append(keypointsList)    
        
    graph(frameList, inputs[1])
    """
    inputs = readFromInput()
    frameList = []
    

    for x in range(0, 13300):
        data = readFromJSON(x, inputs[0])
        #Parse the data into 25 lists of 3 elements (the keypoints)
        keypointsList = parseData(data)
        #Append this data to the frame list
        frameList.append(keypointsList)
    graph(frameList, inputs[1])

if __name__ == "__main__":
    main()