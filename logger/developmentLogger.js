const { createLogger, format, transports } = require("winston");
const { combine, timestamp, printf,splat,simple } = format;

const initializeBotLogger = () => {
  const myFormat = printf(({ level, message, timestamp }) => {
    return `[${timestamp}] ${level}: ${message}`;
  });
  return createLogger({
    level: "debug",
    format: combine(   splat(),
    simple(),timestamp(), myFormat),
    transports: [new transports.Console()],
  });
};

module.exports = initializeBotLogger;
