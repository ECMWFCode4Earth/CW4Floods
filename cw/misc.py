from math import sin, cos, sqrt, atan2, radians

# Miscvellaneous script for crowdwater project

def str_to_num(x):
    for i in range(7):
        if x == f"minus {i}":
            return -i
        elif x == f"plus {i}":
            return i
        else :
            pass

def haversine_dist(c1, c2):

    # approximate radius of earth in km

    R = 6373.0

    lat1 = c1[0] 
    lon1 = c1[1] 
    lat2 = c2[0] 
    lon2 = c2[0]
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance