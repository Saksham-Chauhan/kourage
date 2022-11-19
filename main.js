const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");
const { botToken } = require("./config.json");

const { startInterval } = require("./helper");

const discordClient = new Client({ intents: [GatewayIntentBits.Guilds] });

discordClient.on("ready", async () => {
  console.log(`Logged in as ${discordClient.user.tag}!`);
  startInterval(discordClient);
});

discordClient.login(botToken);
