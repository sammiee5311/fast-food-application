import os
from pprint import pprint
from typing import List

import joblib
import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient

from get_dataset import read_params

CONFIG_PATH = os.path.join("config", "params.yaml")


def get_logged_model_path(runs: pd.DataFrame, registered_model_name: str) -> str:
    lowest = runs["metrics.mae"].sort_values(ascending=True)[0]
    lowest_run_id = runs[runs["metrics.mae"] == lowest]["run_id"][0]

    client = MlflowClient()

    for mv in client.search_model_versions(f"name='{registered_model_name}'"):
        mv = dict(mv)

        if mv["run_id"] == lowest_run_id:
            current_version = mv["version"]
            logged_model_path = mv["source"]
            pprint(mv, indent=4)
            client.transition_model_version_stage(
                name=registered_model_name, version=current_version, stage="Production"
            )
        else:
            current_version = mv["version"]
            client.transition_model_version_stage(
                name=registered_model_name, version=current_version, stage="Staging"
            )

    return logged_model_path


def log_production_model() -> None:
    config = read_params(CONFIG_PATH)

    remote_server = config["mlflow"]["remote_server_uri"]
    model_dir = config["model"]["path"]
    registered_model_name = config["mlflow"]["registered_model_name"]
    experiment_ids = list(
        config["mlflow"]["experiment_ids"].split(",")
    )  # TODO: Need to modify

    mlflow.set_tracking_uri(remote_server)

    runs = mlflow.search_runs(experiment_ids=experiment_ids)

    logged_model_path = get_logged_model_path(runs, registered_model_name)

    loaded_model = mlflow.pyfunc.load_model(logged_model_path)

    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(loaded_model, model_path)


if __name__ == "__main__":
    log_production_model()
