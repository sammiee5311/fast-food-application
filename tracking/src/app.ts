// Initialize jaeger tracing
import path from "path";
import dotenv from "dotenv";
import tracing from "./uilts/tracer";

dotenv.config({ path: path.join(__dirname, "./config/.env") });
const JAEGER_ENDPOINT = process.env.JAEGER_ENDPOINT;

if (JAEGER_ENDPOINT) {
  const tracer = tracing("tracking", JAEGER_ENDPOINT);
}

import express, { Request, Response, NextFunction } from "express";
import { json } from "body-parser";
import cors from "cors";

import orderRoutes from "./routes.orders";
import { tokenValidation } from "./middlewares/auth";
import corsOptions from "./middlewares/cors";
import logger from "./config/logging";

const isTest = process.env.NODE_ENV === "test" ? true : false;

const app = express();

if (isTest) {
  app.use(cors(corsOptions));
}

if (!isTest) {
  app.use(tokenValidation);
}

app.use(json());

app.use("/api/v1", orderRoutes);

app.use((err: Error, req: Request, res: Response, _: NextFunction) => {
  const ip = req.header("x-forwarded-for") || req.socket.remoteAddress;
  logger.error({
    ip: ip,
    method: req.method,
    url: req.url,
    message: err.message,
  });
  res.status(500).json({ message: err.message });
});

export default app;
