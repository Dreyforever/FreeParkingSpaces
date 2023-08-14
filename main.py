import cv2
import numpy as np
import cvzone
import pickle

cap = cv2.VideoCapture('carPark.mp4')
w, h = 107, 45

with open('ParkingPos', 'rb') as f:
    posList = pickle.load(f)

total = len(posList)
free= 0
def Check(NewImg):
    free = 0

    for pos in posList:
        x, y = pos
        imgCrp = NewImg[y:y+h,x:x+w]
        count = cv2.countNonZero(imgCrp)
        if count < 800:
            cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (0, 255, 0), 2)
            cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1, thickness=2, offset=0, colorR=(0, 255, 0))
            free += 1
        else:
            cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (0,0,255), 2)
            cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1, thickness=2, offset=0, colorR=(0,0,255))

    return free



while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgGrey, (3,3), 1)
    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(threshold, 5)

    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(median, kernel, iterations=1)
    free = Check(dilate)

    # for pos in posList:
    cvzone.putTextRect(img, f'Spaces: {free}/{total}', (20,50), scale = 2, thickness=3, offset= 10 , colorR=(0,255,0))
    cv2.imshow("img", img)
    cv2.waitKey(7)