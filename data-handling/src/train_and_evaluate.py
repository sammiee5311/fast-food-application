import os
from dataclasses import dataclass
from typing import Tuple
from urllib.parse import urlparse

import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from get_dataset import ConfigYaml, read_params
from ml_linear import get_elastic_net_model

CONFIG_PATH = os.path.join("config", "params.yaml")


@dataclass
class Data:
    train_x: pd.DataFrame
    train_y: pd.DataFrame
    test_x: pd.DataFrame
    test_y: pd.DataFrame


def eval_metrics(actual: pd.DataFrame, pred: np.array) -> Tuple[float, float, float]:
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)

    return rmse, mae, r2


def has_file_store_in_already(mlflow_uri: str) -> bool:
    tracking_uri_type_store = urlparse(mlflow_uri).scheme

    return tracking_uri_type_store != "file"


def run_mlflow(config: ConfigYaml, data: Data) -> None:
    remote_server = config["mlflow"]["remote_server_uri"]
    experiment_name = config["mlflow"]["experiment_name"]
    run_name = config["mlflow"]["run_name"]
    registered_model_name = config["mlflow"]["registered_model_name"]

    mlflow.set_tracking_uri(remote_server)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name):
        lr = get_elastic_net_model(config)
        lr.fit(data.train_x, data.train_y)

        predicted_delivery_time = lr.predict(data.test_x)
        rmse, mae, r2 = eval_metrics(data.test_y, predicted_delivery_time)

        mlflow.log_params(dict(alpha=lr.alpha, l1_ratio=lr.l1_ratio))
        mlflow.log_metrics(dict(rmse=rmse, mae=mae, r2=r2))

        if has_file_store_in_already(mlflow.get_artifact_uri()):
            mlflow.sklearn.log_model(lr, "model", registered_model_name=registered_model_name)
        else:
            mlflow.sklearn.load_model(lr, "model")


def train_and_evaluate():
    config = read_params(CONFIG_PATH)
    train_data_path = config["data"]["train"]["path"]
    test_data_path = config["data"]["test"]["path"]

    target = [config["data"]["train"]["target"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    data = Data(train_x, train_y, test_x, test_y)

    run_mlflow(config, data)


if __name__ == "__main__":
    train_and_evaluate()
