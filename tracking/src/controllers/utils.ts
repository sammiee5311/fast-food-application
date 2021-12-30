import { Order, Menu } from "../models/order";
import {
  FromDjangoPayload,
  FromRestaurantPayload,
  ToRestaurantPayload,
} from "../models/order";

// TODO: use kafka
// try to get an order from django and check if the restaraunt can make the menus or not
// and then update database. (It can increase dependency ?)
export const kafkaFromDjangoTopic: FromDjangoPayload[] = [];
export const kafkaFromRestaurantTopic: FromRestaurantPayload[] = [];
export const kafkaToRestaurantTopic: ToRestaurantPayload[] = [];

export const orders: Order[] = []; // independent order database from other servers.

export const createPayloadFromRestaurant = (orderId: string) => {
  const availability = [true, false][Math.floor(Math.random() * 2)];
  const payload = new FromRestaurantPayload(orderId, availability);

  kafkaFromRestaurantTopic.push(payload);
};

export const createOrder = (orderId: string, restaurantId: string) => {
  // TODO(maybe): try to generate vid ID gererator api server.

  const orderFromUser = new Order(orderId, restaurantId, false);
  orders.push(orderFromUser);

  createPayloadFromRestaurant(orderId);
};

export const createPayloadFromDjango = (
  menus: Menu[],
  restaurantId: string
) => {
  const payload = new FromDjangoPayload(menus, restaurantId);

  // restaurant server will get the topic and check the menus.
  // to restaraunt producer
  kafkaFromDjangoTopic.push(payload);
};

export const checkRestaurantAvailable = () => {
  // from restaurant consumer
  while (kafkaFromRestaurantTopic.length > 0) {
    const { orderId, availability } = kafkaFromRestaurantTopic.shift()!;

    const matchedOrder = orders.find((order) => orderId === order.id);

    if (matchedOrder) {
      matchedOrder.isAvailable = availability;
    }
  }
};
