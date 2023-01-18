import cv2 as cv
import numpy as np
import time

# getting the video
vid = cv.VideoCapture(0)

# infinite while loop
while (True):
    # scan frame from video
    bull, frame = vid.read()
    # OPERATIONS ON FRAME

    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.blur(frame, (10, 10))  # blur

    # thresholding
    # masks frame to seprate the wanted color
    lower_color = np.array([90, 80, 80])
    upper_color = np.array([150, 255, 255])
    thresholdlow = 100
    thresholdmax = 300
    mask = cv.inRange(hsvframe, lower_color, upper_color)

    # apply mask
    res = cv.bitwise_and(frame, frame, mask=mask)
    # find contour
    cv.bilateralFilter(frame, 12, 100, 100)  # blur to edge
    grayframe = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(grayframe,10,100, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(grayframe, contours=contours, contourIdx=-1, color=(0,0,0), thickness=10, lineType=cv.LINE_AA)

    cordinates = cv.findNonZero(grayframe)

    # results
    print(cordinates)
    cv.imshow("gray",grayframe)
    cv.imshow("frame", frame)
    cv.imshow('res',res)

    # pressing "q" will break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

