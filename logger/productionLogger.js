const { createLogger, format, transports } = require("winston");
const { combine, timestamp, printf,splat,simple } = format;

const myFormat = printf(({ level, message, timestamp }) => {
  return `[${timestamp}] ${level}: ${message}`;
});

const initializeProductionLogger = () => {
  return createLogger({
    level: "info",
    format: combine(   splat(),
    simple(),timestamp(), myFormat),
    transports: [
      new transports.Console(),
      // Use when we want log file
      // new transports.File({ filename: "botErrors.log" }),
    ],
  });
};

module.exports = initializeProductionLogger;
