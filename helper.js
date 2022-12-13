const logger = require("./logger");
const { getReviews } = require("./scrapper");
const { channelID } = require("./config.json");
const { EmbedBuilder } = require("discord.js");

const INTERVAL_TIME = 6 * 60 * 60 * 1000;
let REVIEWS = [];

/**
 * This function fetch the google reviews after every 12 hours and send the latest reviews on discord channel.
 * @param {*} discordClient "Object of discord client."
 */

const startInterval = async (discordClient) => {
  try {
    const { reviews } = await getReviews();
    if (reviews.length) {
      logger.info(
        "Scrapping successfully done and sending reviews on discord."
      );
    }
    if (REVIEWS?.length === 0) {
      REVIEWS = reviews;
      sendMessage(REVIEWS, discordClient);
    } else if (reviews?.length > REVIEWS?.length) {
      const latestReviewsList = [];
      for (let i = 0; i < reviews?.length; i++) {
        if (i > reviews?.length - REVIEWS?.length) {
          break;
        }
        latestReviewsList.push(reviews[reviews?.length - i - 1]);
      }
      if (latestReviewsList?.length)
        sendMessage(latstReviewsList, discordClient);
    }
    setTimeout(startInterval, INTERVAL_TIME);
  } catch (error) {
    logger.error("Error in startInterval:", error);
  }
};

/**
<<<<<<< HEAD
 * This function sends review message to the specified channel
 * @param {Object} disgordClient Object of discord client.
 * @param {Array} reviews "Array of reviews."
 */
const sendMessage = async (reviews, discordClient) => {
  if (reviews?.length) {
    const channel = discordClient.channels.cache.get(channelId);
    reviews?.forEach((element) => {
      if (!element?.snippet) element["snippet"] = "None";
      if (element?.user?.name) {
        const reviewEmbed = new EmbedBuilder()
          .setColor(0x0099ff)
          .setURL(element?.user?.thumbnail)
          .setTitle("⭐".repeat(element?.rating))
          .setAuthor({
            name: element?.user?.name,
            iconURL: element?.user?.thumbnail,
            url: element?.user?.link,
          })
          .setDescription(element?.snippet);
=======
 * Send reviews to discord channel.
 * @param {*} reviews Array of reviews objects.
 * @param {*} discordClient Discord client object.
 */
>>>>>>> d3e21abcc94c4e61db4b75bb84ed78c3b07a51fd

const sendMessage = async (reviews, discordClient) => {
  try {
    if (reviews?.length) {
      const channel = discordClient.channels.cache.get(channelID);
      reviews?.forEach((element) => {
        if (!element?.snippet) element["snippet"] = "None";
        if (element?.user?.name) {
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

module.exports = { startInterval };
