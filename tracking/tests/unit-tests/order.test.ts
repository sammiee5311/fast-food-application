import "jest";
import express from "express";
import request from "supertest";

import app from "../../src/app";

let server: express.Application;

const ORIGIN = "http://localhost:3000";

describe("CreateOrder", () => {
  beforeAll(() => {
    server = app;
  });

  it("return 200 status code", () => {
    return request(server).get("/orders").set("Origin", ORIGIN).expect(200);
  });

  it("return 500 status code", () => {
    return request(server).get("/orders").expect(500);
  });

  it("return 200 from mockData", () => {
    return request(server)
      .get("/orders/mockData")
      .set("Origin", ORIGIN)
      .expect(200);
  });
});
