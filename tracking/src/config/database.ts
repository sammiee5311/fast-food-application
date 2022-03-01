import { Pool, PoolConfig } from "pg";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.join(__dirname, ".env") });

const config: PoolConfig = {
  max: 20,
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: +process.env.DB_PORT!,
  idleTimeoutMillis: 30000,
};

export const connection = new Pool(config);
