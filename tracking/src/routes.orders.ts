import { Router } from "express";

import {
  getOrders,
  postRestaurantRecipes,
  postIngredients,
} from "./controllers.orders";
import log from "./middlewares/log";

const router = Router();

router.use(log);

router.get("/orders", getOrders);

router.post("/recipes", postRestaurantRecipes);

router.post("/ingredients", postIngredients);

export default router;
