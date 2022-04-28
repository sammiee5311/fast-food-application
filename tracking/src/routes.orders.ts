import { Router } from "express";

import { getOrders, postIngredientsByMenus } from "./controllers.orders";
import log from "./middlewares/log";

const router = Router();

router.use(log);

router.get("/orders", getOrders);

router.post("/ingredients", postIngredientsByMenus);

export default router;
