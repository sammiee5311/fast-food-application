class DistanceError(Exception):
    def __init__(self, message="an error while calculating distance"):
        self.message = message
        super().__init__(self.message)


class WeatherError(Exception):
    def __init__(self, message="an error while getting weather info"):
        self.message = message
        super().__init__(self.message)


class APIConnectionError(Exception):
    def __init__(self, message="machine learning api cannot be connected"):
        self.message = message
        super().__init__(self.message)


class OrderNotFound(Exception):
    def __init__(self, message: str = "Order is not found."):
        self.message = message
        super().__init__(self.message)


class EstimatedDeliveryTimeAlreadyExist(Exception):
    def __init__(self, message: str = "Estimated delivery time is already calcuated."):
        self.message = message
        super().__init__(self.message)
