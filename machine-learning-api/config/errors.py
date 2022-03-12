class DataNotExist(AttributeError):
    def __init__(self, message="Data does not exist. Please Check your data."):
        self.message = message
        super().__init__(self.message)


class FeaturesNotSame(Exception):
    def __init__(self, message="Input is not same as expected model features."):
        self.message = message
        super().__init__(self.message)


class FeaturesNotIncluded(Exception):
    def __init__(self, message="Input is included features that are not in expected model features."):
        self.message = message
        super().__init__(self.message)


class FeatureDataError(Exception):
    def __init__(self, message="Feature Data Error"):
        self.message = message
        super().__init__(self.message)
