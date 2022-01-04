import os
import sqlite3
from sqlite3 import Cursor
from typing import Protocol

from utils.env import load_env
from utils.errors import EstimatedDeliveryTimeAlreadyExist, OrderNotFound

load_env()

DB_FILE = os.environ["DB_FILE"]
TABLE = os.environ["DB_TABLE"]


class Database(Protocol):
    def __init__(self, file: str):
        ...

    def __enter__(self) -> Cursor:
        ...

    def __exit__(self, type, value, traceback):
        ...


class SqlLite3:
    def __init__(self, file: str):
        self.file = file

    def __enter__(self) -> Cursor:
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        print("commiting...")
        self.conn.commit()
        print("closing...")
        self.conn.close()


def update_estimated_delivery_time(database: Database, order_id: str, estimated_delivery_time: int) -> None:
    with database(DB_FILE) as cursor:
        cursor.execute(f"SELECT estimated_delivery_time FROM {TABLE} WHERE id = {order_id}")
        result = cursor.fetchone()

        if not result:
            raise OrderNotFound()

        if result[0]:
            raise EstimatedDeliveryTimeAlreadyExist()

        cursor.execute(f"UPDATE {TABLE} SET estimated_delivery_time = {estimated_delivery_time} WHERE id = {order_id}")


if __name__ == "__main__":
    update_estimated_delivery_time(SqlLite3, order_id=2, estimated_delivery_time=2)