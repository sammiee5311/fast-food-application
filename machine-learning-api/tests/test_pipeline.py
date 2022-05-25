import os
import sys

import pandas as pd

sys.path.append(f"{os.getcwd()}/src/")
from click.testing import CliRunner
from src.get_dataset import get_dataset
from src.load_dataset import load_and_save_dataset
from src.split_dataset import get_information, split_dataset


def test_get_dataset() -> None:
    data = get_dataset()

    assert isinstance(data, pd.DataFrame)


def test_save_dataset(config) -> None:
    runner = CliRunner()
    result = runner.invoke(load_and_save_dataset)

    raw_data_path = config["data"]["raw"]["path"]

    assert result.exit_code == 0
    assert os.path.isfile(raw_data_path)


def test_split_dataset(config) -> None:
    runner = CliRunner()
    result = runner.invoke(split_dataset)

    train_data_path, test_data_path = get_information(config)[:2]

    assert result.exit_code == 0
    assert os.path.isfile(train_data_path) and os.path.isfile(test_data_path)
