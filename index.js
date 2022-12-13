const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");
require('dotenv').config()

const { startInterval } = require("./helper");
const logger = require("./logger");

const discordClient = new Client({ intents: [GatewayIntentBits.Guilds] });

discordClient.on("ready", async () => {
  try {
    logger.info(`Logged in as ${discordClient.user.tag}!`);
    startInterval(discordClient);
  } catch (error) {
    logger.error("Error during Login:", error);
  }
});
console.log("process.env.botToken", process.env.botToken);
discordClient.login(process.env.botToken);
