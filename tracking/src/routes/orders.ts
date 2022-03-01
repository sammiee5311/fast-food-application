import { Router } from "express";

import { getOrders, connectDatabase } from "../controllers/orders";

const router = Router();

router.get("/", getOrders);

router.get("/database", connectDatabase);

export default router;
