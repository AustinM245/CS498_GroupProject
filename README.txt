Purpose: To create a program that processes the data from JSON
files that contain keypoints from individual bodyparts in OpenPose, and pass
them into various machine learning algorithms to accurately which
letters from American sign language are being displayed.

Files:
-main.py
The main program, which runs all other user stories.

-KNN.py
Implements our custom KNN algorithm

-Erratic_Movement_Dataset_Tests.py
Implements our algorithms to an erratic dataset, to see how our algorithms work
on data that is not as simple and currated.

-Keypoint folders
Contains all of the data outputted from OpenPose.

Compilation: Run main.py in an IDE such as Spyder. Requires data in the form of 
JSON files to be processed. The data should be in folders organized like so:
YourName_Keypoints\A
YourName_Keypoints\B
...
YourName_Keypoints\Z
These should be in the same directory as the program. As of the moment, there is no way
for the user to select a YourName_Keypoints folder. This will be implemented in a future UI.

Output: This prototype outputs the accuracy scores on training and testing sets from three
machine learning algorithms. The sets are randomized every time the program is run, giving
different accuracy scores. The algorithms train themselves on the training sets, then
are tested against with the testing sets, which they have never seen before. The idea is to know
if the algorithm is good at working with data it has never seen before, therefore, the testing set 
gives a better idea of how good each algorithm is.