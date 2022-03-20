import { Ingredients, OrderMenu, Recipes } from "../types";
import mongoDb from "../config/database/mongoDb";

const getIngredientQuantity = (
  current: number,
  ingredientQuantity: number,
  menuQuantity: number
) => {
  return ingredientQuantity * menuQuantity + (current ? current : 0);
};

export const isRestaurantAvailable = async (
  menus: OrderMenu[],
  restaurantId: number
) => {
  try {
    await mongoDb.connect();
    const restaruant = await mongoDb.getRestaurantRecipes(restaurantId);
    mongoDb.disconnect();

    const recipes = <Recipes>restaruant!.recipes;
    const ingredients = <Ingredients>restaruant!.ingredients;
    const totalIngredientsNeed: Ingredients = {};

    for (const menu of menus) {
      const recipe = recipes[menu.name];

      // TODO: Need to use recursive
      Object.entries(recipe).forEach(([name, ingredient]) => {
        const [quantity, kind] = ingredient.split(" ");
        if (!kind) {
          const recursiveIngredients = recipes[name];
          Object.entries(recursiveIngredients).forEach(([name, ingredient]) => {
            const [quantity, kind] = ingredient.split(" ");
            totalIngredientsNeed[name] = getIngredientQuantity(
              totalIngredientsNeed[name],
              +quantity,
              menu.quantity
            );
          });
        } else {
          totalIngredientsNeed[name] = getIngredientQuantity(
            totalIngredientsNeed[name],
            +quantity,
            menu.quantity
          );
        }
      });
    }

    Object.entries(totalIngredientsNeed).forEach(
      ([ingredientNeed, quantity]) => {
        if (ingredients[ingredientNeed] < quantity) return false;
        ingredients[ingredientNeed] -= quantity;
      }
    );

    return true;
  } catch (err) {
    console.log(err);
    mongoDb.disconnect();
    return false;
  }
};
