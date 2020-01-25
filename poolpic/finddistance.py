import evtech
import cv2
import json
from math import sin, cos, sqrt, atan2, radians

path = "/local/2020_hackathon/2020_hackathon/12996748"

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



with open("/local/2020_hackathon/2020_hackathon/12996748/12996748.geojson") as f:
    data = json.load(f)

    for feature in data['features']:
        #prints "Polygon"
        #print(feature['geometry']['type'])
        firsttime = True
        counter = 0
        for point in feature['geometry']['coordinates'][0]:
            
            
            #check starting point and move to next set of points if it is a starting point
            if firsttime == True:
                pt1Lat = point[0]
                pt1Lon = point[1]
                firsttime = False
                counter += 1
                continue
            else:
                pt2Lat = pt1Lat
                pt2Lon = pt1Lon

                pt1Lat = point[0]
                pt1Lon = point[1]

                print(pt1Lat)
                print(pt1Lon)
                print(pt2Lat)
                print(pt2Lon)
                firsttime = True

            
            print("Printing dimensions from point " + str(counter) + " to " + str(counter + 1))
            measurement = getDistance(pt1Lat, pt1Lon, pt2Lat, pt1Lon)
            
            print("Measurement made: " + str(measurement))
            print()
            counter += 1
        print("\n\nFinished polygon\n\n")
        #print(feature['geometry']['coordinates'])
        #break
