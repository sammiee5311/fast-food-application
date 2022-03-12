import os

import pytest
from utils.db import SqlLite3

DB_TABLE = os.environ["DB_TABLE"]


@pytest.fixture
def clear_database(order_id: str):
    with SqlLite3() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET estimated_delivery_time = 0 WHERE id = '{order_id}'")
