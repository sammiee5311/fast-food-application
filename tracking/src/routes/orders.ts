import { Router } from "express";

import {
  getOrders,
  postAddDjangoTopic,
  getConsumeOrderFromDjango,
  getCheck,
} from "../controllers/orders";

const router = Router();

router.get("/", getOrders);

router.post("/", postAddDjangoTopic);

router.get("/consume", getConsumeOrderFromDjango);

router.get("/check", getCheck);

export default router;
