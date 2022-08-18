export interface OrderMenu {
  name: string;
  price: number;
  quantity: number;
}

export interface Order {
  id: string;
  menus: OrderMenu[];
  restaurant: number;
}

export interface Restaurant {
  _id: number;
  name: string;
  recipes: Recipes;
  ingredients: Ingredients;
}

export interface IngredientsInRecipe {
  [ingredient: string]: string;
}

export interface Ingredients {
  [ingredient: string]: number;
}

export interface Recipes {
  [recipe: string]: IngredientsInRecipe;
}

export interface KafkaOrderMessage {
  id: string;
  username: string;
  user: number;
  user_zipcode: string;
  created_on_str: string;
  menus: OrderMenu[];
  total_price: number;
  restaurant: number;
  restaurant_zipcode: string;
  restaurant_name: string;
  estimated_delivery_time: null | number;
  delivery_time: null | number;
}

export interface JwtData {
  token_type?: string;
  exp?: number;
  iat?: number;
  jti?: string;
  user_id?: number;
  username?: string;
}

export type MongoConfigParams = "user" | "password" | "host" | "port";
