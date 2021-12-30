import express, { Request, Response, NextFunction } from "express";
import { json } from "body-parser";

import orderRoutes from "./routes/orders";

const app = express();

app.use(json());

app.use("/orders", orderRoutes);

app.use((err: Error, req: Request, res: Response, _: NextFunction) => {
  res.status(500).json({ message: err.message });
});

app.listen(3001);
