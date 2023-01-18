import cv2 as cv
import numpy as np

# getting the video
vid = cv.VideoCapture(0)

# infinite while loop
while (True):
        # scan frame from video
        bull, frame = vid.read()

        # OPERATIONS ON FRAME
        hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        blur = cv.blur(frame, (10, 10))  # blur
        # thresholding
        # masks frame to seprate the wanted color
        lower_color = np.array([90, 80, 80])
        upper_color = np.array([150, 255, 255])
        mask = cv.inRange(hsvframe, lower_color, upper_color)

        # apply mask and get it rdy for contour detection
        res = cv.bitwise_xor(frame, frame, mask=mask)
        result = res
        cv.bilateralFilter(frame, 12, 100, 100)  # blur to edge
        grayframe = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(grayframe,50,100, cv.THRESH_BINARY)#show only pixels with value 50-100
        # find contour
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        print("Number of contours detected:", len(contours))
        cv.drawContours(grayframe, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=5, lineType=cv.LINE_AA)
        cordinates = cv.countNonZero(grayframe)
        #RESULTS
        print(cordinates)
        cv.imshow("gray",grayframe)
        cv.imshow("frame", frame)
        cv.imshow("result", result)
