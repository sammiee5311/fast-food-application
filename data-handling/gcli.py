import click
import requests

FEATURES = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
]
HOST = 000
PORT = 000


@click.group()
def cli():
    """Data Handling"""


@click.command("predict")
@click.option("--data", help="feature data")
@click.option("--host", default=f"https://{HOST}/predict", help="host")
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
