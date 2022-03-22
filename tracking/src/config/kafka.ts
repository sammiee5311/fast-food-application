import { Kafka } from "kafkajs";
import { KafkaOrderMessage, OrderMenu, Restaurant } from "../types/index";
import { getCaculatedRestaurantIngredients } from "../uilts/helper";
import orders from "../models/orders";
import mongoDb from "./database/mongoDb";

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

      if (await isRestaurantAvailable(restaurant, menus)) {
        orders.addNewOrder(id, menus, restaurant);
      }
    },
  });
};

const isRestaurantAvailable = async (
  restaurantId: number,
  menus: OrderMenu[]
) => {
  try {
    await mongoDb.connect();
    const restaurant = (await mongoDb.getRestaurantRecipes(
      restaurantId
    )) as unknown as Restaurant;

    const { ingredients, possible } = getCaculatedRestaurantIngredients(
      menus,
      restaurant
    );

    if (!possible) return false;

    await mongoDb.updateRestaurantIngredientsQuantity(
      restaurantId,
      ingredients
    );

    mongoDb.disconnect();

    return true;
  } catch (err) {
    console.log(err);
    return false;
  }
};

export default startConsumOrders;
