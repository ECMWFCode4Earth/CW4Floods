import pandas as pd
from cw.cfg import DATA_DIR, PLOT_DIR
from cw.data import Data
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pylab as plt
from sklearn.feature_selection import r_regression

import seaborn as sns

ml_data = pd.read_csv(DATA_DIR + "ml_data_v1.csv")

print(ml_data)

sns.pairplot(ml_data)
plt.savefig("test.png")