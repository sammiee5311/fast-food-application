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

export const setTotalAddedIngredients = (
  newIngredients: Ingredients,
  currentIngredients: Ingredients
) => {
  Object.entries(newIngredients).forEach(([ingredient, quantity]) => {
    if (currentIngredients.hasOwnProperty(ingredient)) {
      currentIngredients[ingredient] += +quantity;
    } else {
      currentIngredients[ingredient] = quantity;
    }
  });
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

export const getSqlQuery = (restaurantId: string) => {
  return `SELECT DISTINCT d.name 
          FROM  home_restaurant a, 
                home_restaurant_menu b, 
                home_menu c, 
                home_fooditem d, 
                home_menu_food_items e 
          WHERE a.id = ${restaurantId} 
            AND a.id = b.restaurant_id 
            AND c.id = b.menu_id
            AND c.id = e.menu_id 
            AND d.id = e.fooditem_id`;
};
