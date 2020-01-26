#!/usr/bin/env python3
#Written by Nick Graca, Logan Murdock
#Adam Reitz helped and Owen Siebert supervized
#Made for Hack.tiff on 1/25/2020
#Purpose: Find and compute areas of pools give a top down image!

#need to use evtech
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import json

import evtech
#random
import cv2
from math import *
import glob

#Logan gave this to me to calculate the distance between top left and top right points of the image######
#########################################################################################################
def getDistance(_lat1, _long1, _lat2, _long2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(_lat1)
    lon1 = radians(_long1)
    lat2 = radians(_lat2)
    lon2 = radians(_long2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    #print("Result:", distance)
    #print("Should be:", 278.546, "km")
    #1km = 3280.84 feet 
    return 3280.84 * distance
###########################################################################################################


#Adam Wrote this part and I kept it for the most part######################################################
###########################################################################################################
#loads all nadir and oblique images in a given dataset
#datasetPath ="/local/2020_hackathon/2020_hackathon/22434356"
datasetPath = input("Enter path to dataset: ")
nadirs, obliques = evtech.load_dataset(datasetPath)

ndr=[]
pools=[]
cornerCoords=[]
areas=[]
#code to read all images in as numpy arrays.
for i in range(len(nadirs)):
    #notice a diffrent loader has to be used, default that is provided does not work as intended.
    ndr.append(nadirs[i].load_image(imread))
    cornerCoords.append(nadirs[i].geo_bounds)
############################################################################################################

#This was all me and it was a lot so take it one step at a time and we will get through this together#######
############################################################################################################
for x in range(len(ndr)):
    #takes number from logans func and calculates pixels per foot so I can calculate area in feet^2
    dis = getDistance(cornerCoords[x][0], cornerCoords[x][1], cornerCoords[x][0], cornerCoords[x][3])
    rows, cols, band = np.shape(ndr[0])
    ppf = abs(dis/rows)

    #This is where things get hairy
    #Converts RGB to HSV because it works?
    hsv = cv2.cvtColor(ndr[x], cv2.COLOR_BGR2HSV)
    #Since I am looking for Pools I want colors of blue, that is specified below
    lower_blue = np.array([0,0,40])
    upper_blue = np.array([80, 110, 255])
    #Mask is a high contrast image of pools
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #res is like mask but it has the OG pool colors and black background
    res = cv2.bitwise_and(ndr[x],ndr[x], mask=mask)
    #Canny detects edges from res and the values set say how strict it should be, I dont think i use this...
    edges = cv2.Canny(res,100,600)
    #threshold takes things that are close togther and decides if it should combine them based on values set
    ret,thresh = cv2.threshold(mask,200,255,1)
    #Depending on how strict thres is, this finds all the pools and makes them objects that you can interact with
    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    #Loops through all possible pools, if it is under 21 sqft, probably not a pool... depends on the noise tho
    for i in range(len(contours)):
        cnt = contours[i]
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        area = (cv2.contourArea(approx))*ppf
        #if it is a pool then add it to the list
        if (area > 21):
            pools.append(cnt)

    #Loops through all pools and makes the images
    for y in range(len(pools)-1):
        cnt = pools[y].copy()
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        area = (cv2.contourArea(approx))*ppf
        cp = res.copy()
        img = cv2.drawContours(cp, pools, y, (0,255,0), 3)
        if (area in areas):
            continue
        print("Area:", area, "ft^2")
        areas.append(area)
        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(24,10))
        ax1.imshow(img)
        ax1.axis('off')
        ax2.axis('off')
        ax2.imshow(ndr[x])
        plt.show()
        ax1.clear()
        ax2.clear()
        plt.close()