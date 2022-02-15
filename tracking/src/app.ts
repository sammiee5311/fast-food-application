import express, { Request, Response, NextFunction } from "express";
import { json } from "body-parser";
import cors from "cors";

import orderRoutes from "./routes/orders";
import corsOptions from "./uilts/cors";

const isTest = process.env.NODE_ENV === "test" ? true : false;

const app = express();

if (isTest) {
  app.use(cors(corsOptions));
}

app.use(json());

app.use("/orders", orderRoutes);

app.use((err: Error, req: Request, res: Response, _: NextFunction) => {
  res.status(500).json({ message: err.message });
});

export default app;
