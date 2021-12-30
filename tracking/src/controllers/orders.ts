import { randomUUID } from "crypto";
import { RequestHandler } from "express";

import { Menu, ToRestaurantPayload } from "../models/order";

import {
  kafkaFromDjangoTopic,
  kafkaFromRestaurantTopic,
  kafkaToRestaurantTopic,
  createPayloadFromDjango,
  createOrder,
  orders,
  checkRestaurantAvailable,
} from "./utils";

export const getOrders: RequestHandler = (_1, res, _2) => {
  res.status(200).json({
    kafkaFromDjangoTopic: kafkaFromDjangoTopic,
    kafkaFromRestaurantTopic: kafkaFromRestaurantTopic,
    orders: orders,
  });
};

export const postAddDjangoTopic: RequestHandler = (req, res, _) => {
  const { menus, restaurantId } = req.body as {
    menus: Menu[];
    restaurantId: string;
  };

  // temporary functions
  createPayloadFromDjango(menus, restaurantId);

  res.status(201).json({
    message: "Added a payload in django Topic successfully.",
    kafkaFromDjangoTopic: kafkaFromDjangoTopic,
  });
};

export const getConsumeOrderFromDjango: RequestHandler = (_1, res, _2) => {
  // from django consumer
  while (kafkaFromDjangoTopic.length > 0) {
    const { menus, restaurantId } = kafkaFromDjangoTopic.shift()!;

    const orderId = randomUUID();

    createOrder(orderId, restaurantId);

    const payload = new ToRestaurantPayload(menus, orderId, restaurantId);

    kafkaToRestaurantTopic.push(payload);
  }

  res.status(200).json({
    message: "Done.",
    kafkaToRestaurantTopic: kafkaToRestaurantTopic,
  });
};

export const getCheck: RequestHandler = (_1, res, _2) => {
  checkRestaurantAvailable();

  res.status(200).json({ message: "Checked.", orders: orders });
};
