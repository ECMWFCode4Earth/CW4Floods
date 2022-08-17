# This script will be delete in the final version. It is here just for the testing code
from cw.cfg import DATA_DIR

import pandas as pd

ml_data = pd.read_csv(DATA_DIR + "ml_data_v1.csv")

print(ml_data.efas_dis06.min())
