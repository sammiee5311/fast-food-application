// TODO: Need to implement with database.

export interface Menu {
  name: string;
  quantity: number;
}

export class Order {
  readonly id: string;
  readonly restaurantId: string;
  isAvailable: boolean;

  constructor(id: string, restaurantId: string, isAvailable: boolean = false) {
    this.id = id;
    this.restaurantId = restaurantId;
    this.isAvailable = isAvailable;
  }
}

export class FromDjangoPayload {
  menus: Menu[];
  readonly restaurantId: string;

  constructor(menus: Menu[], restaurantId: string) {
    this.menus = menus;
    this.restaurantId = restaurantId;
  }
}

export class ToRestaurantPayload {
  constructor(
    readonly menus: Menu[],
    private orderId: string,
    private restaurantId: string
  ) {}
}

export class FromRestaurantPayload {
  constructor(readonly orderId: string, readonly availability: boolean) {}
}
