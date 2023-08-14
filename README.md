# FreeParkingSpaces
This is a Computer Vision project the counts the number of free parking spaces that are available in a parking lot. The program checks the video feed and constantly updates the number of free parking slots. The program also takes into account not to include any pedestrians that happen to be on the parking slot, to be seen as an occupied parking space. This is made sure by using a suitable threshold for identifying a free parking space.

Note: 
1. main.py is the main file that has to be run to see the results of the program
2. ParkingPos is the pickle file that has all the coordinates of the parking spaces that are present in the parking lot
3. carPark.mp4 is the video that has been used to test the code
4. carParking.png is the image that has been used to create the pickle file by manually marking alle the possible parking spaces.


The required libraries are : Opencv-python, pickle, numpy, cvzone
