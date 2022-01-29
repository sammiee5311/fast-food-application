import os
import sqlite3
from sqlite3 import Cursor
from typing import Protocol, Union

import psycopg2

from utils.env import load_env
from utils.errors import EstimatedDeliveryTimeAlreadyExist, OrderNotFound

load_env()

DB_FILE = os.environ["DB_FILE"]
DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_TABLE = os.environ["DB_TABLE"]


class Database(Protocol):
    def __enter__(self) -> Cursor:
        ...

    def __exit__(self, type, value, traceback):
        ...


class SqlLite3:
    def __enter__(self) -> Cursor:
        self.conn = sqlite3.connect(DB_FILE)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        print("commiting...")
        self.conn.commit()
        print("closing...")
        self.conn.close()


class PostgreSQL:
    def __enter__(self) -> Cursor:
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, host=DB_HOST, password=DB_PASSWORD)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        print("commiting...")
        self.conn.commit()
        print("closing...")
        self.conn.close()


DATABASE_TYPE = Union[SqlLite3, PostgreSQL]


def update_estimated_delivery_time(database: DATABASE_TYPE, order_id: str, estimated_delivery_time: int) -> None:
    with database() as cursor:
        cursor.execute(f"SELECT estimated_delivery_time FROM {DB_TABLE} WHERE id = '{order_id}'")
        result = cursor.fetchone()

        if not result:
            raise OrderNotFound()

        if result[0]:
            raise EstimatedDeliveryTimeAlreadyExist()

        cursor.execute(
            f"UPDATE {DB_TABLE} SET estimated_delivery_time = {estimated_delivery_time} WHERE id = '{order_id}'"
        )


if __name__ == "__main__":
    update_estimated_delivery_time(PostgreSQL, order_id=2, estimated_delivery_time=2)
