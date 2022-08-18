import path from "path";
import dotenv from "dotenv";
import { MongoClient, Collection } from "mongodb";
import { MongoMemoryServer } from "mongodb-memory-server";

import { Ingredients, Restaurant, MongoConfigParams } from "../../types";

/* istanbul ignore file */

dotenv.config({ path: path.join(__dirname, "../.env") });

const isTest = process.env.NODE_ENV === "test" ? true : false;

const mongoConfig: Record<MongoConfigParams, string | number> = {
  user: process.env.DB_USER!,
  password: process.env.DB_PASSWORD!,
  host: process.env.DB_MG_HOST!,
  port: +process.env.DB_MG_PORT!,
};

const mongoURL = `mongodb://${mongoConfig.user}:${mongoConfig.password}@${mongoConfig.host}:${mongoConfig.port}/`;

class MongoDb {
  public client: MongoClient | undefined;
  constructor() {}

  createClient(URL: string = mongoURL) {
    this.client = new MongoClient(URL);
  }

  getCollection(collectionName: string = "restaurants") {
    const database = this.client!.db("database");
    const collection = <Collection>database.collection(collectionName);

    return collection;
  }

  async connect() {
    await this.client!.connect();
  }

  async disconnect() {
    await this.client!.close();
  }

  async getResult() {
    const collection = this.getCollection();
    const counts = await collection.countDocuments();

    return counts;
  }

  async getRestaurantRecipes(restaurantId: number) {
    const collection = this.getCollection();
    const query = { _id: restaurantId };
    const restaruant = await collection.findOne(query);

    return restaruant!;
  }

  async updateRestaurantIngredientsQuantity(
    restaurantId: number,
    ingredients: Ingredients
  ) {
    const query = { _id: restaurantId };
    const collection = this.getCollection();

    await collection.updateOne(query, {
      $set: { ingredients: ingredients },
    });
  }
}

export default new MongoDb();
