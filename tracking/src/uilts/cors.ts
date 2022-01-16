import cors, { CorsOptions } from "cors";

const WHITELIST = ["http://localhost:3000"];

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
