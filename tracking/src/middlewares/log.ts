import { Request, Response, NextFunction } from "express";

import logger from "../config/logging";

const log = (req: Request, res: Response, next: NextFunction) => {
  const ip = req.header("x-forwarded-for") || req.socket.remoteAddress;
  let message: string = "";
  if (req.url === "/") {
    message = "Getting orders";
  } else if (
    req.url === "/postgre" ||
    req.url === "/mongo" ||
    req.url === "/mockData"
  ) {
    message = `Connecting ${req.url.slice(1)}...`;
  }
  logger.info({
    ip: ip,
    method: req.method,
    url: req.url,
    message: message,
  });

  next();
};

export default log;
