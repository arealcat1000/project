import cv2 as cv
import numpy as np
import time

# getting the video
vid = cv.VideoCapture(0)

# infinite while loop
while (True):
    # scan frame from video
    bull, frame = vid.read()
    # w = int (vid.get(cv.CAP_PROP_FRAME_WIDTH))
    # h = int (vid.get(cv.CAP_PROP_FRAME_HEIGHT))
    # img = np.zeros((h,w,3), np.uint8)

    # OPERATIONS ON FRAME

    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.blur(frame, (10, 10))  # blur

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
    extra_limit = cv.bitwise_and(extra_frame, extra_frame, mask=mask2)
    res = cv.bitwise_and(extra_limit, frame, mask=mask)
    result = res
    # find contour
    cv.bilateralFilter(frame, 12, 100, 100)  # blur to edge
    grayframe = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(grayframe, 100, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #find triangle
    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.1 * cv.arcLength(cnt, True), True)
        if len(approx) == 3:
            triangle = cv.drawContours(result, [cnt], -1, (0, 255, 255), 3)

            # compute the center of mass of the triangle
            M = cv.moments(cnt)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
            cv.putText(result, 'Triangle', (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cordinates = cv.findNonZero(grayframe)

    # results
    # cv.imshow("img",img)
    cv.imshow("extra", extra_limit)
    cv.imshow("frame", frame)
    # cv.imshow("edges", edges)
    cv.imshow("result", result)

    # pressing "q" will break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

