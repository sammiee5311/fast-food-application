import click

from get_dataset import get_dataset, read_params


@click.command("get")
@click.option("--config_path", default="config/params.yaml", help="Config path")
def load_and_save_dataset(config_path: str):
    """Load dataset."""
    config = read_params(config_path)
    data = get_dataset(config_path)

    raw_data_path = config["data"]["raw"]["path"]

    data.to_csv(raw_data_path, sep=",", index=False)


if __name__ == "__main__":
    load_and_save_dataset()
