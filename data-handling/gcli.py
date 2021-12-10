import click
import requests
from requests.exceptions import ConnectionError

from utils import get_schema

FEATURES = list(get_schema().keys())
HOST = "localhost"
PORT = "8080"


class DataNotExist(AttributeError):
    def __init__(self, message="Data does not exist. Please Check your data."):
        self.message = message
        super().__init__(self.message)


@click.group()
def cli():
    """Data Handling"""


@click.command("predict")
@click.option("--data", help="feature data")
@click.option("--host", default=f"http://{HOST}:{PORT}/predict", help="host")
def predict_value(data: str, host: str):
    try:
        if not data:
            raise DataNotExist
        _data = list(map(lambda feature: feature.strip(), data.split(",")))

        payload = {key: val for key, val in zip(FEATURES, _data)}

        response_data = requests.post(url=host, json=payload)
    except (ValueError, DataNotExist, ConnectionError) as error:
        click.echo(click.style(f"{error}", bg="red", fg="white"))
        return

    click.echo(click.style(f"Querying host {host} with data: {payload}", bg="black", fg="white"))

    result = response_data.json()

    bg, fg = ("green", "black") if "error" in result else ("red", "white")

    click.echo(click.style(f"Result : {result}", bg=bg, fg=fg))


if __name__ == "__main__":
    predict_value()
