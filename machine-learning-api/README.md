# Machine Learning API (Heroku)

An api server for a prediction result (estimated delivery time)

## run mlfow command

- mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0 -p 1234

## endpoint

- `/predict`
  - request payload
    - `distance` : `float (0 ~ 10)`
    - `current_time` : `int (0 ~ 60 * 24)`
    - `weather` : `string (cloudy, sunny, rainy, windy)`
    - `traffic` : `int (1 ~ 100)`
    - `season` : `string (spring, summer, fall, winter)`
  - response payload
    - `prediction` : `float`
