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

export interface Ingredient {
  [ingredient: string]: string;
}

export interface Recipe {
  [menu: string]: Ingredient[];
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
