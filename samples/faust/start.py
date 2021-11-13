from faker import Faker

import faust
from data import User

fake = Faker()

app = faust.App(
    "myapp",
    broker="kafka://localhost:9092",
)

topic = app.topic("registered-user", value_type=User)


@app.agent(topic)
async def get_register_user(users):
    async for user in users:
        print(f"Registered user: {user.name}, 'address': {user.address}, 'created_at': {user.created_at}")


@app.timer(interval=3.0)
async def send_register_user():
    user = User(name=fake.name(), address=fake.address(), created_at=fake.year())
    await get_register_user.send(value=user)


if __name__ == "__main__":
    app.main()
