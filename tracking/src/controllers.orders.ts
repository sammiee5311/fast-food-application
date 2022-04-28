import { RequestHandler } from "express";

import startConsumOrders from "./config/kafka";

import orders from "./models/orders";
import { Ingredients, Restaurant } from "./types";
import { setTotalAddedIngredients, getSqlQuery } from "./uilts/helper";

import mongoDb from "./config/database/mongoDb";
import postgreDb from "./config/database/postgreDb";

const isProduction = process.env.NODE_ENV === "production" ? true : false;

if (isProduction) startConsumOrders();

export const getOrders: RequestHandler = async (_, res, _2) => {
  res.status(200).json({ message: "Get orders successfully", orders });
};

export const postIngredientsByMenus: RequestHandler = async (
  req,
  res,
  next
) => {
  try {
    const restaurantId: string = req.body.restaurantId;
    const menuName: string = req.body.restaurantMenu;
    const ingredients: Ingredients = req.body.restaurantIngredients;

    await Promise.all([postgreDb.connect(), mongoDb.connect()]);

    const sql = getSqlQuery(restaurantId);

    const restaurantMenus = await postgreDb.getResult(sql);

    if (restaurantMenus.filter((menu) => menu.name === menuName).length === 0) {
      throw new Error(
        "Requested menu does not exist. Please, Check restaurants menus again."
      );
    }

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
      restaurantMenus,
      restaurant,
    });
  } catch (error) {
    next(error);
  } finally {
    await Promise.all([postgreDb.disconnect(), mongoDb.disconnect()]);
  }
};
