import { randomUUID } from "crypto";
import PgMock2 from "pgmock2";

export const rows = [
  {
    id: randomUUID(),
    createdOn: new Date(),
    estimated_delivery_time: 30,
    delivery_time: null,
    restaurant_id: 1,
    user_id: 1,
  },
  {
    id: randomUUID(),
    createdOn: new Date(),
    estimated_delivery_time: 30,
    delivery_time: null,
    restaurant_id: 2,
    user_id: 2,
  },
  {
    id: randomUUID(),
    createdOn: new Date(),
    estimated_delivery_time: 30,
    delivery_time: null,
    restaurant_id: 3,
    user_id: 3,
  },
  {
    id: randomUUID(),
    createdOn: new Date(),
    estimated_delivery_time: 30,
    delivery_time: null,
    restaurant_id: 4,
    user_id: 4,
  },
  {
    id: randomUUID(),
    createdOn: new Date(),
    estimated_delivery_time: 30,
    delivery_time: null,
    restaurant_id: 5,
    user_id: 5,
  },
];

const connection = new PgMock2();

connection.add("SELECT * FROM order_order", [], {
  rowCount: rows.length,
  rows: rows,
});

export default connection;
