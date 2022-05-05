import { Request, Response, NextFunction } from "express";

import fetch, { Headers } from "node-fetch";
import { JwtData } from "../types/index";

export const tokenValidation = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const requestHeaders = new Headers();
  requestHeaders.set("Authorization", <string>req.headers["authorization"]);

  const response = await fetch("http://localhost:8000/api/token/validation", {
    headers: requestHeaders,
  });

  if (response.status === 500) {
    res.status(500).send({ message: "Something went wrong" });
  }

  try {
    const data: JwtData = await response.json();

    if (!("user_id" in data)) {
      throw new Error();
    }
  } catch (err) {
    res.status(402).send({ message: "Invalid token." });
  }

  next();
};
