import cv2 as cv
import numpy as np
import time

# getting the video
vid = cv.VideoCapture(0)

# infinite while loop
while (True):
    # scan frame from video
    bull, frame = vid.read()
    #w = int (vid.get(cv.CAP_PROP_FRAME_WIDTH))
    #h = int (vid.get(cv.CAP_PROP_FRAME_HEIGHT))
    #img = np.zeros((h,w,3), np.uint8)


    # OPERATIONS ON FRAME

    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.blur(frame, (10,10))#blur

    # thresholding
    # masks frame to seprate the wanted color
    lower_color = np.array([90, 80, 80])
    upper_color = np.array([150, 255, 255])
    thresholdlow = 100
    thresholdmax = 300
    extra_frame = frame
    extra_edge = cv.Canny(extra_frame, thresholdlow, thresholdlow, 10)
    hsvextra = cv.cvtColor(extra_frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvextra, lower_color, upper_color)
    mask2 = cv.inRange(hsvframe, lower_color, upper_color)

    # apply mask
    extra_limit =cv.bitwise_and(extra_frame,extra_frame, mask=mask2)
    res = cv.bitwise_and(extra_limit, frame, mask=mask)
    result = res
    # find contour
    cv.bilateralFilter(frame, 12, 100, 100)#blur to edge
    grayframe = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(grayframe, 100, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #differ bitween big and small contour
    list =[]
    for cnt in contours:
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
                    cv.drawContours(result, contours=contours, contourIdx=-1, color=(0,0,255), thickness=1, lineType=cv.LINE_AA)
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
    #cv.imshow("img",img)
    cv.imshow("extra",extra_limit)
    cv.imshow("frame", frame)
    #cv.imshow("edges", edges)
    cv.imshow("result", result)

    # pressing "q" will break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

