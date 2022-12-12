const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");
const { botToken } = require("./config.json");

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

discordClient.login(botToken);
