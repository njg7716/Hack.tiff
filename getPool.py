#!/usr/bin/env python3
#need to use evtech
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import json

import evtech
#random
import cv2
import math
import glob
datasetPath="/local/2020_hackathon/2020_hackathon/12996748"
#loads all nadir and oblique images in a given dataset
nadirs, obliques = evtech.load_dataset(datasetPath)

ndr=[]
obq=[]
#code to read all images in as numpy arrays.
for i in range(len(nadirs)):
    #notice a diffrent loader has to be used, default that is provided does not work as intended.
    ndr.append(nadirs[0].load_image(imread))
for j in range(len(obliques)):
    obq.append(obliques[0].load_image(imread))
    
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,5))

hsv = cv2.cvtColor(ndr[0], cv2.COLOR_BGR2HSV)
lower_blue = np.array([0,0,40])
upper_blue = np.array([80, 90, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(ndr[0],ndr[0], mask=mask)
blue = res[:,:,0]
edges = cv2.Canny(blue,100,600)
ret,thresh = cv2.threshold(edges,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(res,[box],0,(0,0,255),2)
#epsilon = 0.1*cv2.arcLength(cnt,True)
#approx = cv2.approxPolyDP(cnt,epsilon,True)
length = cv2.arcLength(box, True)
area = cv2.contourArea(box)
width = area/length
#img = cv2.drawContours(res, contours, 0, (0,255,0), 3)
print("Length: " + str(length) + " Width: " + str(width) + " Area: " + str(area))

ax1.imshow(im)
ax1.axis('off')
ax2.axis('off')
ax2.imshow(edges)
plt.show()