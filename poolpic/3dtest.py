import evtech
import cv2
import json
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


#JUST COMMENTED THIS OUT
#fig = plt.figure()
#ax = plt.axes(projection='3d')

#ax.plot_surface(x_array, y_array, z_array, cmap='viridis', edgecolor='none')
#ax.set_title('Surface plot')







path = "/home/lxm8708/Hacktiff/poolpic/12996748"








with open("/home/lxm8708/Hacktiff/poolpic/12996748/12996748.geojson") as f:
#with open("/local/2020_hackathon/2020_hackathon/12996748/12996748.geojson") as f:
    data = json.load(f)

    #Loop through polygons
    for feature in data['features']:
        x_array = []
        y_array = []
        z_array = []
        #prints "Polygon"
        #print(feature['geometry']['type'])
        firsttime = True
        counter = 0
        for point in feature['geometry']['coordinates'][0]:
            
            
            #check starting point and move to next set of points if it is a starting point
            if firsttime == True:
                pt1Lat = point[0]
                pt1Lon = point[1]
                pt1Alt = point[2]
                firsttime = False
                counter += 1
                continue
            else:
                x_array.append(pt1Lat)
                y_array.append(pt1Lon)
                z_array.append(pt1Lat)
                
                pt2Lat = pt1Lat
                pt2Lon = pt1Lon
                pt2Alt = pt1Alt

                pt1Lat = point[0]
                pt1Lon = point[1]
                pt1Alt = point[2]

                #print(pt1Lat)
                #print(pt1Lon)
                #print(pt2Lat)
                #print(pt2Lon)
                firsttime = True

            
            print("Printing dimensions from point " + str(counter) + " to " + str(counter + 1))
            #measurement = getDistance(pt1Lat, pt1Lon, pt2Lat, pt1Lon)
            
            #print("Measurement made: " + str(measurement))
            #print()
            counter += 1
        print("\n\nFinished polygon\n\n")
        #print(feature['geometry']['coordinates'])
        #break


        #ax.plot_surface(x_array, y_array, z_array, cmap='viridis', edgecolor='none')
        plt.plot(x_array, z_array)#, y_array)
plt.show()
    



