import { RequestHandler } from "express";
import { connection } from "../config/database";
import orders from "../models/orders";
import startConsumOrders from "../config/kafka";

startConsumOrders();

export const getOrders: RequestHandler = async (_1, res, _2) => {
  res.status(200).json(orders);
};

export const connectDatabase: RequestHandler = async (_1, res, _2) => {
  try {
    const client = await connection.connect();

    const sql = "SELECT * FROM order_order";
    const { rows } = await client.query(sql);

    client.release();

    res.status(200).json(rows);
  } catch (error) {
    res.status(400).json(error);
  }
};
