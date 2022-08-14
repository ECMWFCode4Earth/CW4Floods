import pandas as pd
import numpy as np
from typing import List

class Data(object):
    def __init__(self, data:pd.DataFrame) -> None:
        self.ml_data = data
        self.root_id = data.ROOT_ID.unique()
        self.info()

    def info(self):

        reading_frequency = np.unique(self.ml_data.ROOT_ID, return_counts = True)
        sorted_freq = sorted(zip(reading_frequency[1], reading_frequency[0]), reverse=True)
        
        print(f"There are total {len(sorted_freq)} stations")
        print(f"Maxinmum and minimum number of readings for a station is {sorted_freq[0][0]} and {sorted_freq[-1][0]}")
        print(f"The total number of readings are {len(self.ml_data)}")

    def _get_ml_df(self, data, root_id:int):
        
        mask = data["ROOT_ID"] == root_id

        test_data = data[mask]
        train_data = data[~mask]

        return train_data, test_data

    def get_ml_data(self, keep:List = []):
        data_list = []
        keep.extend(["ROOT_ID", "efas_dis06"])
        data = self.ml_data.filter(keep)

        for id in self.root_id:
            train_data, test_data = self._get_ml_df(data, id)
            
            y_train = train_data["efas_dis06"].values
            x_train =train_data.drop(columns = ["efas_dis06",]).values             
            
            y_test = test_data["efas_dis06"].values
            x_test =test_data.drop(columns = ["efas_dis06",]).values             
            
            ml_data = MLData(id, (x_train, y_train), (x_test, y_test))

            data_list.append(ml_data)

        return data_list

class MLData(object):
    def __init__(self, station_id, train, test) -> None:
        self.test_station_id = station_id
        self.x_train = train[0]
        self.x_test = test[0]

        self.y_train = train[1]
        self.y_test = test[1]
