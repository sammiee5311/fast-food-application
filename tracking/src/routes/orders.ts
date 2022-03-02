import { Router } from "express";

import {
  getOrders,
  connectDatabase,
  connectMockDatabase,
} from "../controllers/orders";

const router = Router();

router.get("/", getOrders);

router.get("/database", connectDatabase);

router.get("/mockDatabase", connectMockDatabase);

export default router;
