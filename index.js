const { Client, GatewayIntentBits, EmbedBuilder } = require("discord.js");
require('dotenv').config()
const schedule = require('node-schedule');

const discordClient = new Client({ intents: [GatewayIntentBits.Guilds] });

discordClient.on("ready", async () => {
    try {
        console.log(`Logged in as ${discordClient.user.tag}!`);
        const job = schedule.scheduleJob(process.env.CRON, async function(){
            const channel = discordClient.channels.cache.get(process.env.CHANNEL);
            await channel.send(process.env.CONTENT);
          });
    } catch (error) {
        console.log("Error during Login:", error);
    }
});

discordClient.login(process.env.TOKEN);


