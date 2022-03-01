import { OrderMenu, Order } from "../types";

class Orders {
  private orders: Order[] = [];
  constructor() {
    this.orders = [];
  }
  addNewOrder(id: string, menus: OrderMenu[], restaurant: number) {
    const newOrder = { id, menus, restaurant };
    this.orders.push(newOrder);
  }
}

export default new Orders();
