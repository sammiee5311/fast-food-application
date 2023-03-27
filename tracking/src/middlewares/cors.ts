import { CorsOptions } from "cors";

const WHITELIST = ["http://127.0.0.1:3000", "http://127.0.0.1:3001"];

const corsOptions: CorsOptions = {
  origin: (origin, callback) => {
    if (WHITELIST.indexOf(<string>origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error("Not Allowed Origin."));
    }
  },
};

export default corsOptions;
