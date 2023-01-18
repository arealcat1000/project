import cv2 as cv
import numpy as np
import time

# getting the video
vid = cv.VideoCapture(0)

# infinite while loop
while (True):
    # scan frame from video
    bull, frame = vid.read()
    w = int (vid.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int (vid.get(cv.CAP_PROP_FRAME_HEIGHT))
    img = np.zeros((h,w,3), np.uint8)
    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # operations on frame
    # blur
    blu = cv.bilateralFilter(frame, 9, 75, 75)  # blur

    # thresholding
    # masks frame to seprate the wanted color
    lower_color = np.array([90, 80, 80])
    upper_color = np.array([150, 255, 255])
    hsvdst = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvframe, lower_color, upper_color)
    # apply mask
    res = cv.bitwise_and(frame, frame, mask=mask)
    # blur image for better color detection

    blur = cv.bilateralFilter(frame, 12, 100, 100)

    result = res
    # find edge
    thresholdlow = 100
    thresholdmax = 300
    edge = cv.Canny(res, thresholdlow, thresholdlow, 3)
    edges = cv.bitwise_and(res, res, mask=edge)
    grayframe = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    #find contour
    ret, thresh = cv.threshold(grayframe, 100, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #differ bitween big and small contour
    list =[]
    for cnt in contours:
        perimeter = cv.arcLength(cnt, True)
        if perimeter ==  True :

            area = cv.contourArea(cnt)
            list.append(area)
            print(len(contours))
            print("contours")
            #time.sleep(5)
            print(len(list))
            print("list")
            if len(list) == len(contours):
                max_area = max(list)
                if  area == max_area :
                    cv.drawContours(result, contours=contours, contourIdx=-1, color=(255,0, 0), thickness=1, lineType=cv.LINE_AA)
                    print("ya mom")


    '''
    cordinates = cv.findNonZero(grayframe)


    
    xmin = min(cordinates)
    ymin = min(cordinates)
    print(xmin, ymin)
    print("-----------")
    print(cordinates)
    '''
    # results
    cv.imshow("img",img)
    cv.imshow("frame", frame)
    #cv.imshow("edges", edges)
    cv.imshow("result", result)

    # pressing "q" will break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

