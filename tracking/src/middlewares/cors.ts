import { CorsOptions } from "cors";

const WHITELIST = ["http://localhost:3000", "http://localhost:3001"];

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
