import { OrderMenu, Recipes } from "../types";

class Restaurant {
  id: number;
  recipes: Recipes[];
  constructor(id: number, recipes: Recipes[]) {
    this.id = id;
    this.recipes = recipes;
  }
  checkIfMenuAvailable(menus: OrderMenu[]) {
    // TODO: check availability in database
  }
}

export default Restaurant;
