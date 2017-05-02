import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

def checkDist(contour1,contour2):
    shape1,shape2 = contour1.shape[0],contour2.shape[0]
    for i in xrange(shape1):
        for j in xrange(shape2):
            dist = np.linalg.norm(contour1[i]-contour2[j])
            if abs(dist) < 50 :
                return True
            elif i==shape1-1 and j==shape2-1:
                return False

def centerBox((cx, cy, cw, ch)):
    w2 = (200-cw)/2
    h2 = (200-ch)/2

    newX = cx - w2
    newY = cy - h2

    return (newX, newY)

def resize(count): 
    img = cv2.imread('/Users/Mat/Desktop/bebop10/' + str('%04d'%count) + '.jpg')
    img = cv2.resize(img, (448, 448))
    cv2.imwrite('/Users/Mat/Desktop/bebop10/' + str('%04d'%count) + '.jpg', img)

def getBB(count, text_file):
    # Import images
    background = cv2.imread('/Users/Mat/Desktop/bebop10/0000.jpg')
    #background = imutils.resize(background, width = 500)
    drone = cv2.imread('/Users/Mat/Desktop/bebop10/' + str('%04d'%count) + '.jpg')
    #drone = imutils.resize(drone, width = 500 )

    # Find any moving pieces by subtracting out the background 
    diff = cv2.absdiff(background, drone)

    # Threshold the image 
    thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    thresh = cv2.dilate(thresh, np.ones((6,6),np.uint8), iterations=2)
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    highArea = 0 

    for c in contours: 
        if cv2.contourArea(c) > highArea:
            highArea = cv2.contourArea(c)
            highC = c

    #for c in contours:
     #   if cv2.contourArea(c) < 500:
      #      continue

        #(x, y) = centerBox(cv2.boundingRect(c))
        #rects.append(cv2.boundingRect(c))
    (x, y, w, h) = cv2.boundingRect(highC)
    #cv2.rectangle(drone, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Output to file 
    text_file.write(str(x) + ' ' +  str(y) + ' ' + str(w) + ' ' + str(h) + ' ' + '\n')

    #rects, _ = cv2.groupRectangles(rects, 1, 0.65)
    #print(rects)	

    # Crop around drone 
    #newDrone = drone[y:y+199,x:x+199]

    #cv2.imshow('test.jpg', drone)
    #for r in rects: 
	#(x, y, w, h),_ = r
	#cv2.rectangle(drone, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow('dilate', thresh)
    #cv2.imshow('detect', drone)

    #cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #output = open('/Users/Mat/Desktop/bebop10/Labels.txt', "w")

    resize(0)

    for i in range(1, 169):
        resize(i)
        output = open('/Users/Mat/Desktop/bebop10/' + str('%04d'%i) + '.txt', "w")
        getBB(i, output)
        output.close()



