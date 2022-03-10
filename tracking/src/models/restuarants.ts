import { OrderMenu, Recipe } from "../types";

class Restaurant {
  id: number;
  recipes: Recipe[];
  constructor(id: number, recipes: Recipe[]) {
    this.id = id;
    this.recipes = recipes;
  }
  checkIfMenuAvailable(menus: OrderMenu[]) {
    // TODO: check availability in database
  }
}

export default Restaurant;
