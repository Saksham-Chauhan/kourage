const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");
require('dotenv').config()
const schedule = require('node-schedule');
const logger = require("./logger");

const discordClient = new Client({ intents: [GatewayIntentBits.Guilds] });

discordClient.on("ready", async () => {
    try {
        logger.info(`Logged in as ${discordClient.user.tag}!`);
         schedule.scheduleJob('* * * * *',async function(){
            const channel = discordClient.channels.cache.get(process.env.channelID);
            await channel.send('The answer to life, the universe, and everything!');
            logger.info("Webhook send with content:'The answer to life, the universe, and everything!'");
          });
    } catch (error) {
        logger.error(`Error during sending webhook and error is: ${error}`);
    }
});

discordClient.login(process.env.botToken);