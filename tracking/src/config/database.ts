import { Pool, PoolConfig } from "pg";
import path from "path";
import dotenv from "dotenv";

import PgMock2 from "pgmock2";
import { rows } from "./mockData";

dotenv.config({ path: path.join(__dirname, ".env") });

const isTest = process.env.NODE_ENV === "test" ? true : false;

const postgreConfig: PoolConfig = {
  max: 20,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  port: +process.env.DB_PG_PORT!,
  idleTimeoutMillis: 30000,
};

let connection: PgMock2 | Pool;

if (isTest) {
  connection = new PgMock2();
  connection.add("SELECT * FROM order_order", [], {
    rowCount: rows.length,
    rows: rows,
  });
} else {
  connection = new Pool(postgreConfig);
}

export default connection;
