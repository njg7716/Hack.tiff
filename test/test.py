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
datasetPath="12854744"
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
ax1.imshow(ndr[0])
ax1.axis('off')
ax2.axis('off')
ax2.imshow(obq[0])
plt.show()

#finds all json files in a given directory and imports data as a dict
jsonFiles=glob.glob(datasetPath+"/nadirs/*.json")
jsonFiles.append(glob.glob(datasetPath+"/obliques/*.json"))
print(jsonFiles)
#use multiple indexs here to ensure this works
with open(jsonFiles[0]) as data:
    jsonData = json.load(data)
#demonstrating ability to create camrea model from json    
camera1=evtech.camera.camera_from_json(jsonData)
print("projection matrix:",camera1.projection_matrix,
"\nimage center:",camera1.image_center,
"\nimage bounds:",camera1.image_bounds,
"\ngeo bounds:",camera1.geo_bounds,
"\nelevation:",camera1.elevation,
"\ncrs:",camera1.crs,
"\nImage Path:",camera1.image_path)

#using camera model derived above to project ground coordinates to focal plane (i think?)
coords=camera1.project_to_camera(-95.1504, 29.48927, 5)
newCoords=(math.floor(coords[0]),math.floor(coords[1]))
print(newCoords)
copy=ndr[0].copy()
cv2.circle(copy, newCoords, 2, [255,0,0], 2)
plt.imshow(copy)
plt.axis('off')
plt.show()

#using a number between 80 and 84 does supply the user with some useful information however...
print(evtech.geodesy.utm_crs_from_latlon(82, 29.489192871931156))



