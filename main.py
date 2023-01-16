import cv2 as cv
import numpy as np

offset = abs(10)
#getting the video
vid = cv.VideoCapture(0)

#infinite while loop
while (True):
    #scan frame from videor
    bull ,frame = vid.read()
    hsvframe =cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # operations on frame
    #blur
    blu = cv.bilateralFilter(frame,9,75,75)#blur

    #thresholding
    #masks frame to seprate the wanted color
    lower_color = np.array([90, 80, 80])
    upper_color = np.array([150, 255, 255])
    hsvdst = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvframe, lower_color, upper_color)
    #apply mask
    res = cv.bitwise_and(frame, frame, mask=mask)
    #blur image for better color detection

    blur = cv.bilateralFilter(frame, 10, 100, 100)

    result= res


    # find countour
    thresholdlow =100
    thresholdmax =300
    edge = cv.Canny(res,thresholdlow,thresholdlow,3)
    edges=cv.bitwise_and(res,res,mask=edge)

    cv.bilateralFilter(frame, 5, 75, 75)#blur

    grayframe = cv.cvtColor(edges,cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(grayframe, 100, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(frame, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=1, lineType=cv.LINE_AA)

    cordinates = cv.findNonZero(grayframe)

    xmin = min(cordinates)
    ymin = min(cordinates)
    print (xmin,ymin)
    print("-----------")
    print(cordinates)

    #results
    cv.imshow("frame",frame)
    cv.imshow("edges",edges)
    cv.imshow('grayscale',grayframe)
    cv.imshow("result",result)


    #pressing "q" will break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()


