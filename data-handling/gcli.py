import click
import requests

from utils import get_schema

FEATURES = list(get_schema().keys())
HOST = "localhost"
PORT = "8080"


@click.group()
def cli():
    """Data Handling"""


@click.command("predict")
@click.option("--data", help="feature data")
@click.option("--host", default=f"http://{HOST}:{PORT}/predict", help="host")
def predict_value(data: str, host: str):
    _data = list(map(lambda feature: feature.strip(), data.split(",")))

    try:
        payload = {key: val for key, val in zip(FEATURES, _data)}
    except ValueError as error:
        click.echo(click.style(f"{error}", bg="red", fg="white"))
        return

    click.echo(click.style(f"Querying host {host} with data: {payload}", bg="black", fg="white"))
    result = requests.post(url=host, json=payload)

    if "error" in result.json():
        click.echo(click.style(f"Result : {result.json()}", bg="red", fg="white"))
    else:
        click.echo(click.style(f"Result : {result.json()}", bg="green", fg="black"))


if __name__ == "__main__":
    predict_value()
