import pandas as pd
from cw.cfg import DATA_DIR, PLOT_DIR
from cw.data import Data
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pylab as plt
from sklearn.feature_selection import r_regression

ml_data = pd.read_csv(DATA_DIR + "ml_data_v2.csv")

raw_data = Data(ml_data)

data = raw_data.get_ml_data(["HEIGHT1[cm]","SPOTTED_AT", 'WIDTH[m]', "ORDER", "AREA[m2]"])

model = "rf"


for each_data in data:
    x_train = each_data.x_train
    x_test = each_data.x_test
    
    y_train = each_data.y_train
    y_test = each_data.y_test
    
    if model == "lin_reg":
        reg = LinearRegression().fit(x_train,y_train)
    elif model == "rf":
        reg = RandomForestRegressor().fit(x_train,y_train)

    y_pred_test = reg.predict(x_test)
    y_pred_train = reg.predict(x_train) 

    fig, (ax1, ax2) = plt.subplots(1, 2)
    


    ax1.scatter(y_train, y_pred_train, s = 1.5, label = f"r : {r_regression(y_train.reshape(-1, 1), y_pred_train.reshape(-1, 1))[0]:.2f}")
    ax1.set_xlabel("Obs")
    ax1.set_ylabel("Pred")
    ax1.legend()
    ax2.scatter(y_test, y_pred_test, s = 1.5, label = f"r : {r_regression(y_test.reshape(-1, 1), y_pred_test.reshape(-1, 1))[0]:.2f}")
    ax2.set_xlabel("Obs")
    ax2.set_ylabel("Pred")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(PLOT_DIR+f"{model}_{each_data.test_station_id}.png")
    plt.close()

 