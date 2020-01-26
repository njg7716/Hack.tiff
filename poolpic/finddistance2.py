import evtech
import cv2
import json
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import argparse

# Load arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d",
                    "--dataset",
                    help="Location of dataset",
                    type=str)
args = parser.parse_args()

path = args.dataset#"/home/lxm8708/Hacktiff/poolpic/12996748"
jsonpath = path + '/' + path.split('/')[-1] + '.geojson'

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
    
    #convert to feet
    return 3280.84 * distance

def midpoint(_lat1, _long1, _lat2, _long2):
    midx = (_lat1 + _lat2) / 2
    midy = (_long1 + _long2) / 2
    return midx, midy


def dist3D(dist1, z1, z2):  
    #pythagorean theorum to get distance of slanted roof points
    result = dist1 * dist1 + (z1 - z2) * (z1 - z2)
    return sqrt(result)

    




with open(jsonpath) as f:
    data = json.load(f)

    #Loop through polygons and draw every side
    for feature in data['features']:
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
                x_array = []
                y_array = []

                x_array.append(pt1Lat)
                y_array.append(pt1Lon)
                
                pt2Lat = pt1Lat
                pt2Lon = pt1Lon
                pt2Alt = pt1Alt


                pt1Lat = point[0]
                pt1Lon = point[1]
                pt1Alt = point[2]

                midpointx , midpointy = midpoint(pt1Lat, pt1Lon, pt2Lat, pt2Lon)

                x_array.append(midpointx)
                y_array.append(midpointy)

                x_array.append(pt1Lat)
                y_array.append(pt1Lon)

                firsttime = True

            
            measurement = getDistance(pt1Lat, pt1Lon, pt2Lat, pt2Lon)
            measurement = dist3D(measurement, pt1Alt, pt2Alt)
            
            
            counter += 1
            temp = plt.plot(x_array, y_array, label=str('%.1f' % measurement) + " ft")
            
            #adding labels at the midpoints of the lines
            plt.annotate(str('%.1f' % measurement) + " ft",(midpointx,midpointy)) 

plt.axis('off')
plt.show()
    


#Provided test code used to display the image used
########################################################################################
# Only care about nadirs for this app
nadirs, obliques = evtech.load_dataset(path)
# Load first oblique image
img = nadirs[0].load_image()
# Making Window For The Image
cv2.namedWindow("Image")
# Starting The Loop So Image Can Be Shown
while(True):
    cv2.imshow("Image",img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
########################################################################################