from cw.cfg import DATA_DIR
from cw.io import read_cw_data
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

cw_data = read_cw_data()

keep = ['ROOT_ID', 'LATITUDE', 'LONGITUDE', 'WATER_LEVEL', 'SPOTTED_AT']
cw_data = cw_data.filter(keep)

cw_data = cw_data[cw_data.WATER_LEVEL.notna()]
cw_data = cw_data[cw_data.WATER_LEVEL != "false" ]

reading_frequency = np.unique(cw_data.ROOT_ID, return_counts = True)
sorted_freq = sorted(zip(reading_frequency[1], reading_frequency[0]), reverse=True)
tuples = zip(*sorted_freq)
freq, station_id = [ list(tuple) for tuple in tuples]

# Add frequency_data

index = [i for i, val in enumerate(freq) if val>1]
station_id = [station_id[i] for i in index]

# Let us create a dataset for 100 stations with data

cw_data = cw_data[cw_data.ROOT_ID.isin(station_id[:100])]

station_ind = pd.read_csv(DATA_DIR + "station_ind_v1.tsv", delimiter="\t")

merged_data = cw_data.merge(station_ind, on="ROOT_ID")

merged_data.to_csv(DATA_DIR + "cw_data_with_shortlist_lat_lon_index_v1.csv", index = False)