import { Ingredients, OrderMenu, Recipes, Restaurant } from "../types";

const getIngredientQuantity = (
  current: number,
  ingredientQuantity: number,
  menuQuantity: number
) => {
  return ingredientQuantity * menuQuantity + (current ? current : 0);
};

const setTotalIngredientsNeed = (
  menu: OrderMenu,
  totalIngredientsNeed: Ingredients,
  recipes: Recipes
) => {
  const recipe = recipes[menu.name];
  const queue = [recipe];

  while (queue.length > 0) {
    const recipe = queue.shift()!;
    Object.entries(recipe).forEach(([name, ingredient]) => {
      const [quantity, kind] = ingredient.split(" ");
      if (!kind) {
        queue.push(recipes[name]);
      } else {
        totalIngredientsNeed[name] = getIngredientQuantity(
          totalIngredientsNeed[name],
          +quantity,
          menu.quantity
        );
      }
    });
  }
};

export const getCaculatedRestaurantIngredients = (
  menus: OrderMenu[],
  restaruant: Restaurant
) => {
  const recipes = <Recipes>restaruant!.recipes;
  const ingredients = <Ingredients>restaruant!.ingredients;
  const totalIngredientsNeed: Ingredients = {};
  let possible = true;

  for (const menu of menus) {
    setTotalIngredientsNeed(menu, totalIngredientsNeed, recipes);
  }

  for (const [ingredientNeed, quantity] of Object.entries(
    totalIngredientsNeed
  )) {
    if (ingredients[ingredientNeed] < quantity) {
      possible = false;
      break;
    }
    ingredients[ingredientNeed] -= quantity;
  }

  return { ingredients, possible };
};
