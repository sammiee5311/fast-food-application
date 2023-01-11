import { Request, Response, NextFunction } from "express";

import fetch, { Headers } from "node-fetch";
import opentelemetry from "@opentelemetry/api";
import { JwtData } from "../types/index";
import tracer from "../utils/tracing";
import { Span, ROOT_CONTEXT } from "@opentelemetry/api";

/* istanbul ignore file */

export const tokenValidation = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const requestHeaders = new Headers();
    const span = tracer.startSpan("auth-validation");
    opentelemetry.propagation.inject(ROOT_CONTEXT, {});
    requestHeaders.set("Authorization", <string>req.headers["authorization"]);

    if (span.isRecording()) {
      (span as Span).setAttribute(
        "authorization",
        <string>req.headers["authorization"]
      );
    }

    const response = await fetch(
      "https:/nginx-proxy/api/v0/token/validation/",
      {
        headers: requestHeaders,
      }
    );

    span.end();

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
