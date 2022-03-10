import path from "path";
import dotenv from "dotenv";
import { MongoClient, Collection } from "mongodb";

dotenv.config({ path: path.join(__dirname, ".env") });

const MONGO_CONFIG = {
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  port: +process.env.DB_MG_PORT!,
};

class MongoDb {
  public client: any = null;
  public config: any = MONGO_CONFIG;

  constructor() {}

  connect() {
    const mongoURI = `mongodb://${this.config.user}:${this.config.password}@${this.config.host}:${this.config.port}/`;
    const client = new MongoClient(mongoURI);
    this.client = client;
  }

  async disconnect() {
    await this.client.close();
  }

  async getCollection() {
    await this.client.connect();

    const database = this.client.db("database");
    const collection = <Collection>database.collection("restaurants");

    return collection;
  }
}

export default new MongoDb();
