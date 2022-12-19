import { RequestHandler } from "express";

import startConsumOrders from "./config/kafka";

import orders from "./models/orders";
import { Ingredients, Restaurant } from "./types";
import { setTotalAddedIngredients } from "./utils/helper";

import mongoDb from "./config/database/mongoDb";

const isProduction = process.env.NODE_ENV === "production" ? true : false;

if (isProduction) {
  startConsumOrders();
  mongoDb.createClient();
}

export const getOrders: RequestHandler = async (_, res, _2) => {
  res.status(200).json({ message: "Get orders successfully", orders });
};

export const postRestaurantRecipes: RequestHandler = async (req, res, next) => {
  try {
    const restaurantId: string = req.body.restaurantId;
    await mongoDb.connect();

    const recipes = await mongoDb.getRestaurantRecipes(+restaurantId);

    res
      .status(200)
      .json({ message: "Get restaurant recipes successfully", recipes });
  } catch (error) {
    next(error);
  } finally {
    await mongoDb.disconnect();
  }
};

export const postIngredients: RequestHandler = async (req, res, next) => {
  try {
    const restaurantId: string = req.body.restaurantId;
    const ingredients: Ingredients = req.body.restaurantIngredients;

    await mongoDb.connect();

    const restaurant = (await mongoDb.getRestaurantRecipes(
      +restaurantId
    )) as unknown as Restaurant;

    setTotalAddedIngredients(ingredients, restaurant.ingredients);

    await mongoDb.updateRestaurantIngredientsQuantity(
      +restaurantId,
      restaurant.ingredients
    );

    res.status(201).json({
      message: "Add ingredients successfully",
      restaurant,
    });
  } catch (error) {
    next(error);
  } finally {
    await mongoDb.disconnect();
  }
};
