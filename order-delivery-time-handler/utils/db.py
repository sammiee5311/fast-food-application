import os
import sqlite3
from sqlite3 import Cursor
from typing import Protocol, Union

import psycopg2
from config.env import load_env
from config.errors import EstimatedDeliveryTimeAlreadyExist, OrderNotFound
from utils.tracing import tracer

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
    with tracer.start_as_current_span("update-EDT") as span:
        with database() as cursor:
            cursor.execute(f"SELECT estimated_delivery_time FROM {DB_TABLE} WHERE id = '{order_id}'")
            result = cursor.fetchone()

            if not result:
                raise OrderNotFound()

            if result[0]:
                raise EstimatedDeliveryTimeAlreadyExist()

            sql_statement = (
                f"UPDATE {DB_TABLE} SET estimated_delivery_time = {estimated_delivery_time} WHERE id = '{order_id}'"
            )

            cursor.execute(sql_statement)

            if span.is_recording():
                span.set_attribute("sql-statement", sql_statement)


if __name__ == "__main__":
    update_estimated_delivery_time(PostgreSQL, order_id=2, estimated_delivery_time=2)
