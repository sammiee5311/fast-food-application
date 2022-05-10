import { jest } from "@jest/globals";
import { MongoMemoryServer } from "mongodb-memory-server";
import mongoDb from "../../src/config/database/mongoDb";

import { Order } from "../../src/types";

export interface ResponseText {
  message: string;
  orders?: { orders: Order[] };
}

export const ORIGIN_URL = "http://localhost:3000";

let mongoTestDB: MongoMemoryServer;

const TIMEOUT = 10000;

declare global {
  namespace jest {
    interface Matchers<R> {
      toHasProperty(data: string): R;
    }
  }
}

const initCustomTestSettings = () => {
  jest.setTimeout(TIMEOUT);

  expect.extend({
    toHasProperty(resJson: ResponseText, data: string) {
      if (resJson.hasOwnProperty(data)) {
        return {
          message: () => `${data} is in response object`,
          pass: true,
        };
      } else {
        return {
          message: () => `expected ${data} in response object`,
          pass: false,
        };
      }
    },
  });
};

export const connectTestDB = async () => {
  mongoTestDB = await MongoMemoryServer.create();
  const testMongoURL = mongoTestDB.getUri();

  mongoDb.createClient(testMongoURL);
};

export const disconnectDB = async () => {
  try {
    if (mongoTestDB) {
      await mongoTestDB.stop();
    }
  } catch (err) {
    console.log(err);
  }
};

export default initCustomTestSettings;
