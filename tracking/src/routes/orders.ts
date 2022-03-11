import { Router } from "express";

import {
  getOrders,
  connectPostgreDB,
  connectMongoDB,
  connectMockDB,
} from "../controllers/orders";
import log from "../middlewares/log";

const router = Router();

router.use(log);

router.get("/", getOrders);

router.get("/postgre", connectPostgreDB);

router.get("/mongo", connectMongoDB);

router.get("/mockData", connectMockDB);

export default router;
