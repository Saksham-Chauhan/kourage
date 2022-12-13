const { EmbedBuilder } = require("discord.js");
const path = require("path");
const fs = require("fs");

const logger = require("./logger");
const { getReviews } = require("./scrapper");
const { channelID } = require("./config.json");

const INTERVAL_TIME = 12 * 60 * 60 * 1000;

/**
 * This function fetch the google reviews after every 12 hours and send the latest reviews on discord channel.
 * @param {*} discordClient "Object of discord client."
 */

const startInterval = async (discordClient) => {
  try {
    const { reviews } = await getReviews();
    if (reviews?.length) {
      logger.info(
        "Scrapping successfully done!"
      );
    }
    const fileReviews = await readFromFile();
    if (fileReviews === null) {
      logger.info(
        "Sending All review first time"
      );
      sendMessage(reviews, discordClient);
      writeInFile(reviews);
    } else if (reviews?.length > fileReviews.length) {
      writeInFile(reviews);
      const noOfLatestReview = reviews?.length - fileReviews?.length;
      let count = 0;
      let latestReviewsList = [];

      reviews.every((item) => {
        fileReviews.forEach((item2) => {
          if (item?.user?.name === item2?.user?.name) {
            latestReviewsList.push(item);
            count++;
          }
          if (count === noOfLatestReview) return false;
          else return false;
        })
      })
      logger.info(`Find ${latestReviewsList.length} latest review`);
      sendMessage(latestReviewsList, discordClient);
    }
    setTimeout(startInterval, 30 * 1000);
  } catch (error) {
    logger.error("Error in startInterval:", error);
  }
};

/**
 * Send reviews to discord channel.
 * @param {*} reviews Array of reviews objects.
 * @param {*} discordClient Discord client object.
 */

const sendMessage = async (reviews, discordClient) => {
  try {
    if (reviews?.length) {
      const channel = discordClient.channels.cache.get(channelID);
      reviews?.forEach((element) => {
        if (!element?.snippet) element["snippet"] = "None";
        if (element?.user?.name) {
          console.log(element?.user?.name)
          const reviewEmbed = new EmbedBuilder()
            .setColor(0x0099ff)
            .setURL(element?.user?.thumbnail)
            //   .setThumbnail(element?.user?.thumbnail)
            .setTitle("⭐".repeat(element?.rating))
            .setAuthor({
              name: element?.user?.name,
              iconURL: element?.user?.thumbnail,
              url: element?.user?.link,
            })
            .setDescription(element?.snippet);

          channel.send({ embeds: [reviewEmbed] });
        }
      });
      logger.info("Reviews send successfully on discord channel");
    }
  } catch (error) {
    logger.error("Error in 'sendMessage' func and error is:", error);
  }
};

const readFromFile = () => {
  const filePath = path.join(__dirname, "review.json");
  return new Promise((resolve, reject) => {
    try {
      fs.readFile(filePath, "utf8", async (err, jsonString) => {
        if (err) {
          logger.error(
            "Error in readFromFile func during file reading and error is",
            err
          );
          return resolve(null);
        } else {
          let data = null;
          if (jsonString) data = JSON.parse(jsonString);
          logger.info("File read successfully!");
          return resolve(data);
        }
      });
    } catch (error) {
      logger.error("Error in readFromFile func and error is", error);
      resolve(null);
    }
  });
};

const writeInFile = (data) => {
  const filePath = path.join(__dirname, "review.json");
  return new Promise((resolve, reject) => {
    try {
      fs.writeFile(filePath, JSON.stringify(data), (err) => {
        if (err) {
          logger.error("Error in writeInFile func and error is:", err);
        } else {
          logger.info("File write successfully!");
          resolve(true);
        }
      });
    } catch (error) {
      logger.error("Error in writeInFile func and error is", error);
      resolve(false);
    }
  });
};

module.exports = { startInterval };
