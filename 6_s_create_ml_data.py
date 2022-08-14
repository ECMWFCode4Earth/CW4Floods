import pandas as pd
from cw.io import read_cw_data, read_efas_data
from cw.cfg import DATA_DIR
import numpy as np
from cw.misc import str_to_num

station_data = pd.read_csv(DATA_DIR + "station_with_efas_v1.csv")
stream_info = pd.read_csv(DATA_DIR + "stream_info.csv", delimiter=";")

merged_df = station_data.merge(stream_info, on="ROOT_ID")

merged_df.WATER_LEVEL = merged_df.WATER_LEVEL.map(str_to_num)

merged_df.to_csv(DATA_DIR + "ml_data_v1.csv", index = False)