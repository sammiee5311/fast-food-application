import { Router } from "express";

import { getOrders } from "../controllers/orders";
import log from "../middlewares/log";

const router = Router();

router.use(log);

router.get("/", getOrders);

export default router;
