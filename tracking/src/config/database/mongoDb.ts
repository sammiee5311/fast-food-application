import path from "path";
import dotenv from "dotenv";
import { MongoClient, Collection } from "mongodb";

/* istanbul ignore file */

dotenv.config({ path: path.join(__dirname, "../.env") });

const mongoConfig = {
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  port: +process.env.DB_MG_PORT!,
};

const mongoURL = `mongodb://${mongoConfig.user}:${mongoConfig.password}@${mongoConfig.host}:${mongoConfig.port}/`;

class MongoDb {
  public client: MongoClient = new MongoClient(mongoURL);

  constructor() {}

  async connect() {
    await this.client.connect();
  }

  async disconnect() {
    await this.client.close();
  }

  async getResult() {
    const database = this.client.db("database");
    const collection = <Collection>database.collection("restaurants");
    const counts = await collection.countDocuments();

    return counts;
  }
}

export default new MongoDb();
