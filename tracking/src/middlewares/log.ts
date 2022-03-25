import { Request, Response, NextFunction } from "express";

import logger from "../config/logging";

const log = (req: Request, _: Response, next: NextFunction) => {
  const ip = req.header("x-forwarded-for") || req.socket.remoteAddress;
  logger.info({
    ip: ip,
    method: req.method,
    url: req.url,
    message: "Getting orders",
  });

  next();
};

export default log;
