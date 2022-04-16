import { RequestHandler } from "express";

import startConsumOrders from "../config/kafka";

import orders from "../models/orders";

import mongoDb from "../config/database/mongoDb";
import postgreDb from "../config/database/postgreDb";

const isTest = process.env.NODE_ENV === "test" ? true : false;

if (!isTest) startConsumOrders();

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
    const ingredients: { [menu: string]: { ingredient: number } } =
      req.body.restauranIngredients;

    await Promise.all([postgreDb.connect(), mongoDb.connect()]);

    const sql = `SELECT DISTINCT d.name 
                 FROM  home_restaurant a, 
                       home_restaurant_menu b, 
                       home_menu c, 
                       home_fooditem d, 
                       home_menu_food_items e 
                 WHERE a.id = ${restaurantId} 
                   AND a.id = b.restaurant_id 
                   AND c.id = b.menu_id
                   AND c.id = e.menu_id 
                   AND d.id = e.fooditem_id`;

    const restaurantMenus = await postgreDb.getResult(sql);

    if (restaurantMenus.filter((menu) => menu.name === menuName).length === 0) {
      throw new Error(
        "Requested menu does not exist. Please, Check restaurants menus again."
      );
    }

    res.status(201).json({
      message: "Add ingredients successfully",
      restaurantMenus,
    });
  } catch (error) {
    next(error);
  } finally {
    await Promise.all([postgreDb.disconnect(), mongoDb.disconnect()]);
  }
};
