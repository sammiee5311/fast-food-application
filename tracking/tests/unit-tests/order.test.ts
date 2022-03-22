import "jest";
import express from "express";
import request from "supertest";
import { getCaculatedRestaurantIngredients } from "../../src/uilts/helper";

import app from "../../src/app";
import { OrderMenu, Restaurant } from "../../src/types";

let server: express.Application;

const ORIGIN = "http://localhost:3000";

describe("Server api test", () => {
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

  it("Order 2 kind of menuㄴ and 1 quantity and less than ingredients restaurant have", () => {
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
