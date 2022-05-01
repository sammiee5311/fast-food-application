import { Router } from "express";

import {
  getOrders,
  postRestaurantRecipes,
  postIngredientsByMenus,
} from "./controllers.orders";
import log from "./middlewares/log";

const router = Router();

router.use(log);

router.get("/orders", getOrders);

router.post("/recipes", postRestaurantRecipes);

router.post("/ingredients", postIngredientsByMenus);

export default router;
