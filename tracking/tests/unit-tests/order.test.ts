import "jest";
import express from "express";
import request from "supertest";

import { Menu, FromDjangoPayload } from "../../src/models/order";
import app from "../../src/app";

let server: express.Application;
let menu: Menu;
let payload: FromDjangoPayload;

describe("CreateOrder", () => {
  beforeAll(() => {
    server = app;
    menu = { name: "pizza", quantity: 1 };
    payload = { menus: [menu], restaurantId: "1" };
  });

  it("return 201 status code", () => {
    return request(server)
      .post("/orders")
      .set("Origin", "http://localhost:3000")
      .set("Accept", "application/json")
      .send(payload)
      .expect(201);
  });

  it("return 200 status code", () => {
    return request(server)
      .get("/orders")
      .set("Origin", "http://localhost:3000")
      .expect(200);
  });

  it("return 500 status code", () => {
    return request(server).get("/orders").expect(500);
  });

  it("payload.menus === menus", () => {
    return request(server)
      .get("/orders/consume")
      .set("Accept", "application/json")
      .set("Origin", "http://localhost:3000")
      .expect((res: request.Response) => {
        const resJson = JSON.parse(res.text);
        return resJson.kafkaToRestaurantTopic[0].menus === payload.menus;
      });
  });

  it("return 200", () => {
    return request(server)
      .get("/orders/check")
      .set("Origin", "http://localhost:3000")
      .expect(200);
  });
});
