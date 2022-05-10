import "jest";
import express from "express";
import request from "supertest";

import app from "../../src/app";

import initCustomTestSettings, {
  ORIGIN_URL,
  connectTestDB,
  disconnectDB,
} from "./customSettings";

import { setTotalAddedIngredients } from "../../src/uilts/helper";

let server: express.Application;

initCustomTestSettings();

// TODO: need to implement with api call
describe("Add Ingredients", () => {
  beforeAll(async () => {
    server = app;
    await connectTestDB();
  });

  const ingredients = {
    ham: 1,
    bun: 1,
  };

  const newIngredients = {
    lettuce: 1,
  };

  const restaurant = {
    ingredients: {
      ham: 1,
      bun: 1,
    },
  };

  it("Add 1 quantity of ham and 1 quantity of bun to restaurant ingredients.", () => {
    setTotalAddedIngredients(ingredients, restaurant.ingredients);

    expect(restaurant.ingredients).toEqual({ ham: 2, bun: 2 });
  });

  it("Add 1 quantity of new ingredient to restaurant ingredients.", () => {
    setTotalAddedIngredients(newIngredients, restaurant.ingredients);

    expect(restaurant.ingredients).toEqual({
      ham: 2,
      bun: 2,
      lettuce: 1,
    });
  });

  it("Get recipes", async () => {
    const data = { restaruantId: 1 };

    const res: request.Response = await request(server)
      .post("/api/v1/recipes")
      .set("Content-Type", "application/json")
      .set("Origin", ORIGIN_URL)
      .send(data);

    const resJson = JSON.parse(res.text);

    expect(resJson).toHasProperty("message");
  });
  afterAll(async () => {
    await disconnectDB();
  });
});
