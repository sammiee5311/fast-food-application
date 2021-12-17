from typing import Any, Dict

from sklearn.linear_model import ElasticNet, LinearRegression

ConfigYaml = Dict[str, Dict[str, Any]]


def get_elastic_net_model(config: ConfigYaml) -> ElasticNet:
    random_state = config["data"]["train"]["random_state"]
    alpha = config["model"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["model"]["ElasticNet"]["params"]["l1_ratio"]

    elastic_net = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)

    return elastic_net


def get_linear_regression(config: ConfigYaml) -> LinearRegression:
    random_state = config["data"]["train"]["random_state"]

    linear_regression = LinearRegression(random_state=random_state)

    return linear_regression
