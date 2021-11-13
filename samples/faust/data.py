from faker import Faker

import faust

fake = Faker()


class User(faust.Record):
    name: str
    address: str
    created_at: str


def get_registered_user():
    return fake.name(), fake.address(), fake.year()
