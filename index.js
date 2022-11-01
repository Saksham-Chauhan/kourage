require('dotenv').config();

const fs = require('fs');

const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on('ready', async () => {
    console.log(`Logged in as ${client.user.tag}!`);
    const channel = await client.channels.fetch(process.env.CHANNEL_ID);
    const content = fs.readFileSync('./message.txt', 'utf-8');
    channel.send(content);
    setInterval(() => {
        channel.send(content);
    }, process.env.REPEAT_INTERVAL);
});


client.login(process.env.BOT_TOKEN);