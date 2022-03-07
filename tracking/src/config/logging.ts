import { format, createLogger, transports } from "winston";
import winstonDaily from "winston-daily-rotate-file";
import dotenv from "dotenv";
import path from "path";

dotenv.config({ path: path.join(__dirname, ".env") });

interface TransformableInfo {
  [key: string]: any;
  level: string;
  message: string;
}

const LOG_DIR = process.env.LOG_DIR;

const logger = createLogger({
  transports: [
    new winstonDaily({
      level: "info",
      datePattern: "YYYY-MM-DD",
      dirname: LOG_DIR,
      filename: "%DATE%.log",
      maxFiles: 30,
      zippedArchive: true,
    }),
    new winstonDaily({
      level: "info",
      datePattern: "YYYY-MM-DD",
      dirname: `${LOG_DIR}/error`,
      filename: "%DATE%.error.log",
      maxFiles: 30,
      zippedArchive: true,
    }),
  ],
});

if (process.env.NODE_ENV !== "production") {
  logger.add(
    new transports.Console({
      level: "info",
      format: format.combine(
        format.timestamp({
          format: "YYYY-MM-DD HH:mm:ss",
        }),
        format.json(),
        format.colorize(),
        format.printf(
          (info: TransformableInfo) =>
            `${info.timestamp} ${info.ip} [${info.level}]: ${info.method} - ${info.url} - ${info.message}`
        )
      ),
    })
  );
}

export default logger;
