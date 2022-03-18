import { Kafka } from "kafkajs";
import { KafkaOrderMessage } from "../types/index";
import { isRestaurantAvailable } from "../uilts/helper";
import orders from "../models/orders";

/* istanbul ignore file */
const BROKER = "kafka:29092";

const startConsumOrders = async () => {
  const kafka = new Kafka({
    clientId: "fast-food-order",
    brokers: [BROKER],
  });

  const consumer = kafka.consumer({
    groupId: "fast-food-order",
  });

  consumer.connect();

  consumer.subscribe({
    topic: "fast-food-order",
    fromBeginning: true,
  });

  consumer.run({
    eachMessage: async ({ message }) => {
      const { id, menus, restaurant } = <KafkaOrderMessage>(
        JSON.parse(message.value!.toString())
      );

      console.log("Received message", {
        id,
        menus,
        restaurant,
      });

      if (isRestaurantAvailable(id, menus, restaurant)) {
        orders.addNewOrder(id, menus, restaurant);
      }
    },
  });
};

export default startConsumOrders;
