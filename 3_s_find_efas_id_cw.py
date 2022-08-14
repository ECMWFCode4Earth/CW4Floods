from cw.io import read_cw_data, read_efas_data
from cw.cfg import DATA_DIR
import matplotlib.pylab as plt
import numpy as np
from haversine import haversine, Unit

cw_data = read_cw_data()

keep = ['ROOT_ID', 'LATITUDE', 'LONGITUDE', 'WATER_LEVEL', 'SPOTTED_AT']
cw_data = cw_data.filter(keep)

cw_data = cw_data[cw_data.WATER_LEVEL.notna()]
cw_data = cw_data[cw_data.WATER_LEVEL != "false" ]

reading_frequency = np.unique(cw_data.ROOT_ID, return_counts = True)
sorted_freq = sorted(zip(reading_frequency[1], reading_frequency[0]), reverse=True)
tuples = zip(*sorted_freq)
freq, station_id = [ list(tuple) for tuple in tuples]

index = [i for i, val in enumerate(freq) if val>1]
station_id = [station_id[i] for i in index]
cw_data = cw_data[cw_data.ROOT_ID.isin(station_id)]

efas = read_efas_data()

distance_dict = dict()
mask = efas.dis06.mean(axis=0).values
n_station = 0

with open(DATA_DIR + 'station_ind.tsv', "w") as f:
    f.write(f"ROOT_ID\tMinimum Distance (KM)\tLat Index\tLon Index\n")

for index, row in cw_data.iloc[:, :].iterrows():
    if row.ROOT_ID not in distance_dict:
        n_station+=1
        min_d = 2.5   
        for lat_index in range(900):
            for lon_index in range(1000):
                if np.isnan(mask[lat_index, lon_index]) == False :
                    with open(DATA_DIR + 'station_ind.tsv', "a") as f:

                        lat = efas.latitude.values[lat_index][lon_index]
                        lon = efas.longitude.values[lat_index][lon_index]
                        dist = haversine((float(row.LATITUDE), float(row.LONGITUDE)), (lat, lon), unit = Unit.KILOMETERS)
                                            
                        if dist < min_d:
                            min_d = dist
                            f.write(f"{row.ROOT_ID}\t{min_d:.3f}\t{lat_index}\t{lon_index}\n")
                            distance_dict[row.ROOT_ID] = (min_d, lat_index, lon_index)
                else:
                    pass
        
        print(f"{n_station} station discovered")
    else:
        pass