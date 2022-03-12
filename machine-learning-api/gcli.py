from pprint import pprint

import click
import requests
from requests.exceptions import ConnectionError

from config.errors import DataNotExist, FeatureDataError
from utils import get_features_payload, get_schema

FEATURES = get_schema()["required"]
HOST = "localhost"
PORT = "8080"


@click.group()
def cli():
    """Data Handling"""


@click.command("schema")
def schema():
    pprint(get_schema())


@click.command("predict")
@click.option("--data", help=f"{FEATURES}")
@click.option("--host", default=f"http://{HOST}:{PORT}/predict", help="host")
def predict_value(data: str, host: str):
    try:
        if not data:
            raise DataNotExist
        _data = list(map(lambda feature: feature.strip(), data.split(",")))

        payload = get_features_payload(_data)

        response_data = requests.post(url=host, json=payload)
    except (ValueError, DataNotExist, ConnectionError, FeatureDataError) as error:
        click.echo(click.style(f"{error}", bg="red", fg="white"))
        return

    click.echo(click.style(f"Querying host {host} with data: {payload}", bg="black", fg="white"))

    result = response_data.json()

    bg, fg = ("red", "white") if "error" in result else ("green", "black")

    click.echo(click.style(f"Result : {result}", bg=bg, fg=fg))


if __name__ == "__main__":
    cli.add_command(predict_value)
    cli.add_command(schema)
    cli()
