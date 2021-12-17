import os

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from get_dataset import read_params
from ml_linear import get_elastic_net_model

CONFIG_PATH = os.path.join("config", "params.yaml")


def eval_metrics(actual: pd.DataFrame, pred: np.array):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)

    return rmse, mae, r2


def train_and_evaluate():
    config = read_params(CONFIG_PATH)
    train_data_path = config["data"]["train"]["path"]
    test_data_path = config["data"]["test"]["path"]
    model_dir = config["model"]["path"]

    target = [config["data"]["train"]["target"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    lr = get_elastic_net_model(config)

    lr.fit(train_x, train_y)

    predicted_delivery_time = lr.predict(test_x)

    rmse, mae, r2 = eval_metrics(test_y, predicted_delivery_time)

    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(lr, model_path)


if __name__ == "__main__":
    train_and_evaluate()
