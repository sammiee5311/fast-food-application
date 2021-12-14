from subprocess import run

from faker import Faker

import faust

IP_ADDRESS = '127.0.0.1'


class User(faust.Record):
    name: str
    address: str
    created_at: str


fake = Faker()

cnt = 0


app = faust.App("myapp", broker=f"kafka://{IP_ADDRESS}:9092")

topic = app.topic("fast-food-order", value_type=User)


@app.agent(topic)
async def get_register_user(users):
    async for user in users:
        global cnt
        if cnt > 5:
            run(args="ps auxww | grep start | awk '{print $2}' | xargs kill -9", shell=True)
        print(f"Registered user: {user.name}, 'address': {user.address}, 'created_at': {user.created_at}")
        cnt += 1


@app.timer(interval=2.0)
async def send_register_user():
    user = User(name=fake.name(), address=fake.address(), created_at=fake.year())
    await get_register_user.send(value=user)


if __name__ == "__main__":
    app.main()
