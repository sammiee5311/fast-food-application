import click
import requests

FEATURES = [...]


@click.group()
def cli():
    """Data Handling"""


@click.command("predict")
@click.option("--data", help="weather, location, time")
@click.option("--host", default="http://localhost:8080/predict", help="host")
def predict_value(data: str, host: str):
    _data = list(map(lambda feature: feature.strip(), data.split(",")))

    try:
        payload = {key: val for key, val in zip(FEATURES, _data)}
    except ValueError as error:
        click.echo(click.style(f"{error}", bg="red", fg="white"))
        return

    click.echo(click.style(f"Querying host {host} with data: {payload}", bg="black", fg="white"))
    result = requests.post(url=host, json=payload)
    click.echo(click.style(f"Result : {result.json()}"))


if __name__ == "__main__":
    predict_value()
