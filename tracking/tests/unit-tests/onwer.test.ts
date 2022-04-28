import "jest";
import express from "express";

import app from "../../src/app";

import initCustomTestSettings from "./customSettings";

import { setTotalAddedIngredients } from "../../src/uilts/helper";

let server: express.Application;

initCustomTestSettings();

// TODO: need to implement with api call
describe("Add Ingredients", () => {
  beforeAll(() => {
    server = app;
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
});
