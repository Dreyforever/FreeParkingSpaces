import cv2
import numpy as np
import cvzone
import pickle

# enabling the video feed of the parking lot
cap = cv2.VideoCapture('carPark.mp4')

# length and breadth of the parking space
w, h = 107, 45

# opening the pickle file that has the coordinates of all the parking spaces
with open('ParkingPos', 'rb') as f:
    posList = pickle.load(f)

# defining the total and free number of parking spaces
total = len(posList)
free= 0

# Function for checking for a free parking space
def Check(NewImg):
    free = 0

    # Looping through every parking space in the parking lot
    for pos in posList:
        x, y = pos

        # cropping just the image of the parking space and counting the number of sharp pixels in the image
        imgCrp = NewImg[y:y+h,x:x+w]
        count = cv2.countNonZero(imgCrp)

        # defining the threshold for being a free parking space and incrementing the count of free parking spaces
        if count < 800:
            cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (0, 255, 0), 2)
            cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1, thickness=2, offset=0, colorR=(0, 255, 0))
            free += 1
        # defining the threshold of occupied parking spaces
        else:
            cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (0,0,255), 2)
            cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1, thickness=2, offset=0, colorR=(0,0,255))

    return free



while True:

    # Looping the video for a continuous video feed
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    # Converting the image to grey scale
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying guassian blur to smoothen the image
    blur = cv2.GaussianBlur(imgGrey, (3,3), 1)
    # Using adaptive thesholding to find the sharp pixels that are present in the image
    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # Applying median blur to remove salt pepper noises
    median = cv2.medianBlur(threshold, 5)

    kernel = np.ones((3,3),np.uint8)
    # using dilate to enhance the values of the pixels so that there is a better distintion between the sharp pixels
    dilate = cv2.dilate(median, kernel, iterations=1)

    # using the function to check for free parking spaces
    free = Check(dilate)

    cvzone.putTextRect(img, f'Spaces: {free}/{total}', (20,50), scale = 2, thickness=3, offset= 10 , colorR=(0,255,0))
    cv2.imshow("img", img)
    cv2.waitKey(7)
