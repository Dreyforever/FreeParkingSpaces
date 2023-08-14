import cv2
import pickle

# length and breadth of each parking space
w, h = 107, 45

# Loading the pickle file that has the positions of the parking spaces
try:
    with open('ParkingPos', 'rb') as f:
        posList = pickle.load(f)

except:
    posList = []

# Defining the function that will be used to mark the parking spaces manually and load the coordinates of the parking spaces into the pickle file
def mouseClick(events, x, y, flags, para):
    # left click of the mouse is used for marking a parking space and right click of the mouse is used for deletion of a parking space
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+w and y1 < y < y1+h:
                posList.pop(i)

    with open('ParkingPos', 'wb') as f:
        pickle.dump(posList, f)

# Displaying the parking spaces as rectangles in the parking lot image
while True:
    img = cv2.imread('carParkImg.png')

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+w,pos[1]+h), (255,0,255), 2)


    cv2.imshow("Img", img)
    cv2.setMouseCallback("Img",mouseClick)
    cv2.waitKey(1)
