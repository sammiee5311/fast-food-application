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
      .send(payload)
      .set("Accept", "application/json")
      .expect(201);
  });

  it("return 200 status code", () => {
    return request(server).get("/orders").expect(200);
  });

  it("payload.menus === menus", () => {
    return request(server)
      .get("/orders/consume")
      .set("Accept", "application/json")
      .expect((res: request.Response) => {
        const resJson = JSON.parse(res.text);
        return resJson.kafkaToRestaurantTopic[0].menus === payload.menus;
      });
  });

  it("return 200", () => {
    return request(server).get("/orders/check").expect(200);
  });
});
