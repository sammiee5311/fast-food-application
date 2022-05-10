import { Request, Response, NextFunction } from "express";

import fetch, { Headers } from "node-fetch";
import { JwtData } from "../types/index";

/* istanbul ignore file */

export const tokenValidation = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const requestHeaders = new Headers();
    requestHeaders.set("Authorization", <string>req.headers["authorization"]);

    const response = await fetch(
      "https:/nginx-proxy/api/v0/token/validation/",
      {
        headers: requestHeaders,
      }
    );

    if (response.status === 500) {
      res.status(500).json({ message: "Something went wrong" });
    }

    const data: JwtData = await response.json();

    if (!("user_id" in data)) {
      throw new Error();
    }
  } catch (err) {
    res.status(401).json({ message: "Invalid token." });
  }
  next();
};
