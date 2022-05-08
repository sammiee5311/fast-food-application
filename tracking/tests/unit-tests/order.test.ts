import "jest";
import express from "express";
import request from "supertest";

import app from "../../src/app";
import initCustomTestSettings, {
  ORIGIN_URL,
  ResponseText,
} from "./customSettings";
import orders from "../../src/models/orders";
import { getCaculatedRestaurantIngredients } from "../../src/uilts/helper";

import { OrderMenu, Restaurant } from "../../src/types";

let server: express.Application;

initCustomTestSettings();

describe("Server api test", () => {
  beforeAll(() => {
    server = app;
  });

  it("return 200 status code", () => {
    return request(server)
      .get("/api/v1/orders")
      .set("Origin", ORIGIN_URL)
      .expect(200);
  });

  it("return 500 status code", () => {
    return request(server).get("/api/orders").expect(500);
  });

  it("Add 1 order and Get order from api response", async () => {
    const menus: OrderMenu[] = [{ name: "test", price: 5.99, quantity: 1 }];
    const id = "1";
    const restaruant = 1;
    orders.addNewOrder(id, menus, restaruant);

    const res: request.Response = await request(server)
      .get("/api/v1/orders")
      .set("Origin", ORIGIN_URL);

    const resJson = <ResponseText>JSON.parse(res.text);

    expect(resJson).toHasProperty("orders");
    expect(resJson.orders!.orders[0].restaurant).toEqual(1);
  });
});

describe("Restaurant ingredients test", () => {
  const restaruant: Restaurant = {
    _id: 1,
    name: "test",
    recipes: {
      test: {
        a: "1 slice",
        b: "2 slice",
      },
    },
    ingredients: {
      a: 2,
      b: 4,
    },
  };

  it("Order 1 kind of menu and 1 quantity and less than ingredients restaurant have", () => {
    const menus: OrderMenu[] = [{ name: "test", price: 5.99, quantity: 1 }];
    const testRestaurant = JSON.parse(JSON.stringify(restaruant));

    const { ingredients, possible } = getCaculatedRestaurantIngredients(
      menus,
      testRestaurant
    );

    expect(ingredients).toEqual({ a: 1, b: 2 });
    expect(possible).toEqual(true);
  });

  it("Order 1 kind of menu and 4 quantity and greater than ingredients restaurant have", () => {
    const menus: OrderMenu[] = [{ name: "test", price: 5.99, quantity: 4 }];
    const testRestaurant = JSON.parse(JSON.stringify(restaruant));

    const { possible } = getCaculatedRestaurantIngredients(
      menus,
      testRestaurant
    );

    expect(possible).toEqual(false);
  });

  it("Order 2 kind of menu and 1 quantity and less than ingredients restaurant have", () => {
    const menus: OrderMenu[] = [{ name: "test3", price: 5.99, quantity: 1 }];
    const testRestaurant = JSON.parse(JSON.stringify(restaruant));

    testRestaurant.recipes["test2"] = { test: "1" };
    testRestaurant.recipes["test3"] = { test2: "1", c: "1 slice" };
    testRestaurant.ingredients["c"] = 3;

    const { ingredients, possible } = getCaculatedRestaurantIngredients(
      menus,
      testRestaurant
    );

    expect(possible).toEqual(true);
    expect(ingredients).toEqual({ a: 1, b: 2, c: 2 });
  });
});
