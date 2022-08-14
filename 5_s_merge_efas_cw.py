import pandas as pd
from cw.io import read_cw_data, read_efas_data
from cw.cfg import DATA_DIR
import numpy as np

station_ind = pd.read_csv(DATA_DIR + "cw_data_with_shortlist_lat_lon_index_v1.csv")

zeros = np.zeros(len(station_ind))

station_ind["efas_dis06"] = zeros

efas_data = read_efas_data()

station_ind.SPOTTED_AT = station_ind.SPOTTED_AT.map(pd.to_datetime)

for index, row in station_ind.iterrows():
    print(index)
    lat_index = int(row.Lat_Index)
    lon_index = int(row.Lon_Index)
    dt = row.SPOTTED_AT

    dis = efas_data.dis06[:, lat_index, lon_index].sel(time=dt, method="nearest")
    station_ind.iloc[index,-1 ] = dis.values


station_ind.to_csv(DATA_DIR + "station_with_efas_v1.csv", index=False)