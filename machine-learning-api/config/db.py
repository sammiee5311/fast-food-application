import os
import sqlite3

from config.env import load_env
from config.errors import EstimatedDeliveryTimeAlreadyExist, OrderNotFound

load_env()

DB_FILE = os.environ["DB_FILE"]
TABLE = os.environ["DB_TABLE"]


class Database:
    def __init__(self, file: str):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        print("commiting...")
        self.conn.commit()
        print("closing...")
        self.conn.close()


def update_estimated_delivery_time(order_id: str, estimated_delivery_time: int) -> None:
    with Database(DB_FILE) as cursor:
        cursor.execute(f"SELECT estimated_delivery_time FROM {TABLE} WHERE id = {order_id}")
        result = cursor.fetchone()

        if not result:
            raise OrderNotFound()

        if result[0]:
            raise EstimatedDeliveryTimeAlreadyExist()

        cursor.execute(f"UPDATE {TABLE} SET estimated_delivery_time = {estimated_delivery_time} WHERE id = {order_id}")


if __name__ == "__main__":
    update_estimated_delivery_time(order_id=2, estimated_delivery_time=2)
