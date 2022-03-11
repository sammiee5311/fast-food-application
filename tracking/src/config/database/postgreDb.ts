import path from "path";
import dotenv from "dotenv";
import { Pool, PoolConfig, PoolClient } from "pg";

/* istanbul ignore file */

dotenv.config({ path: path.join(__dirname, "../.env") });

const postgreConfig: PoolConfig = {
  max: 20,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  port: +process.env.DB_PG_PORT!,
  idleTimeoutMillis: 30000,
};

class PostgreDb {
  public client: PoolClient | null = null;
  public connection = new Pool(postgreConfig);

  constructor() {}

  async connect() {
    this.client = await this.connection.connect();
  }

  disconnect() {
    if (this.client) this.client.release();
  }

  async getResult(sql: string) {
    const { rows } = await this.client!.query(sql);

    return rows;
  }
}

/* istanbul ignore next */
export default new PostgreDb();
