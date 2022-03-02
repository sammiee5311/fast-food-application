import { RequestHandler } from "express";
import connection from "../config/database";
import orders from "../models/orders";
import startConsumOrders from "../config/kafka";
import { PoolClient } from "pg";
import { IPGClient } from "pgmock2/lib/interfaces";

const isTest = process.env.NODE_ENV === "test" ? true : false;

if (!isTest) startConsumOrders();

export const getOrders: RequestHandler = async (_1, res, _2) => {
  res.status(200).json(orders);
};

/* istanbul ignore next */
export const connectDatabase: RequestHandler = async (_1, res, _2) => {
  try {
    const client = await connection.connect();
    const sql = "SELECT * FROM order_order";

    const { rows } = await (<PoolClient>client).query(sql);

    client.release();

    res.status(200).json(rows);
  } catch (error) {
    res.status(400).json(error);
  }
};

export const connectMockDatabase: RequestHandler = async (_1, res, _2) => {
  try {
    const client = await connection.connect();
    const sql = "SELECT * FROM order_order";

    const { rows } = await (<IPGClient>client).query(sql, []);

    client.release();

    res.status(200).json(rows);
  } catch (error) {
    res.status(400).json(error);
  }
};
