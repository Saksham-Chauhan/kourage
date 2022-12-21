# Introduction 
This functionality sends google business reviews from webpage to your discord channel via scrapping

# Installation
- Node
- Discord.js (Node wrapper for discord)

# How to run
```
npm i
export env variables TOKEN and CHANNEL_ID for windows you can use `set` command
npm run index.js
```

# Docker Usage
```
docker build . -t image_name
docker run -e TOKEN -e CHANNEL -e CONTENT -e CRON image_name
```
TOKEN = Discord token
CONTENT = Content to post
CRON = Cron Schedule (for more search about cron)
CHANNEL = Discord Channel ID (pass id only)

# Contribution
Open issues if you find any other problem

