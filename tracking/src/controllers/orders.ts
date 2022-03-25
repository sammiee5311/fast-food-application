import { RequestHandler } from "express";

import startConsumOrders from "../config/kafka";

import orders from "../models/orders";

const isTest = process.env.NODE_ENV === "test" ? true : false;

if (!isTest) startConsumOrders();

export const getOrders: RequestHandler = async (_, res, _2) => {
  res.status(200).json({ message: "Get orders successfully", orders });
};
