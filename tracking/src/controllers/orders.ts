import { RequestHandler } from "express";
import { PoolClient } from "pg";
import { IPGClient } from "pgmock2/lib/interfaces";

import startConsumOrders from "../config/kafka";
import connection from "../config/database";
import mongoDb from "../config/mongoDb";
import logger from "../config/logging";
import orders from "../models/orders";

const TIMEOUR = 10000;
const isTest = process.env.NODE_ENV === "test" ? true : false;

if (!isTest) startConsumOrders();

jest.setTimeout(TIMEOUR);

export const getOrders: RequestHandler = async (req, res, _2) => {
  const ip = req.header("x-forwarded-for") || req.socket.remoteAddress;

  logger.info({
    ip: ip,
    method: req.method,
    url: req.url,
    message: "Getting orders.",
  });

  res.status(200).json(orders);
};

/* istanbul ignore next */
export const connectDatabase: RequestHandler = async (req, res, _2) => {
  try {
    const ip = req.header("x-forwarded-for") || req.socket.remoteAddress;

    logger.info({
      ip: ip,
      method: req.method,
      url: req.url,
      message: "Connecting database.",
    });

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
  let client: IPGClient | null = null;
  try {
    client = <IPGClient>await connection.connect();

    mongoDb.connect();
    const collection = await mongoDb.getCollection();

    const count = await collection.countDocuments();

    const sql = "SELECT * FROM order_order";
    const { rows } = await (<IPGClient>client).query(sql, []);

    res.status(200).json({ count: count, rows: rows });
  } catch (error) {
    res.status(400).json(error);
  } finally {
    if (client) client.release();
    mongoDb.disconnect();
  }
};
