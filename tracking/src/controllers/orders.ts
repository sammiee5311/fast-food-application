import { RequestHandler } from "express";
import { IPGClient } from "pgmock2/lib/interfaces";

import startConsumOrders from "../config/kafka";
import connection from "../config/mockData";
import postgreDb from "../config/database/postgreDb";
import mongoDb from "../config/database/mongoDb";

import orders from "../models/orders";

import { Order } from "../types";

const isTest = process.env.NODE_ENV === "test" ? true : false;

if (!isTest) startConsumOrders();

export const getOrders: RequestHandler = async (_, res, _2) => {
  res.status(200).json(orders);
};

/* istanbul ignore next */
export const connectPostgreDB: RequestHandler = async (_, res, _2) => {
  try {
    await postgreDb.connect();

    const sql = "SELECT * FROM order_order";
    const rows = await postgreDb.getResult(sql);

    res.status(200).json({ rows: rows });
  } catch (error) {
    res.status(400).json(error);
  } finally {
    postgreDb.disconnect();
  }
};

/* istanbul ignore next */
export const connectMongoDB: RequestHandler = async (_1, res, _2) => {
  try {
    mongoDb.connect();

    const counts = await mongoDb.getResult();

    res.status(200).json({ counts: counts });
  } catch (error) {
    res.status(500).json(error);
  } finally {
    await mongoDb.disconnect();
  }
};

export const connectMockDB: RequestHandler = async (_1, res, _2) => {
  let client: IPGClient | null = null;
  try {
    client = <IPGClient>await connection.connect();

    const sql = "SELECT * FROM order_order";
    const { rows }: { rows: Order[] } = await (<IPGClient>client).query(
      sql,
      []
    );

    res.status(200).json({ rows: rows });
  } catch (error) {
    res.status(500).json(error);
  } finally {
    if (client) client.release();
  }
};
