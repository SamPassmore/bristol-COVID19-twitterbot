# bristol-COVID19-twitterbot

This repo contains a twitter bot to summarise daily COVID-19 statistics in bristol.

Data is drawn from: https://github.com/emmadoughty/Daily_COVID-19

The code can easily be changed to summarise statistics from any UTLA in the UK by changing from the Bristol code on line 50. 
To set up your own bot, you will need a set up access to the twitter API here: https://developer.twitter.com/en

To build the bot: 

Set up the environment and clone the data repository using:

    make install

Check for updates in the data repository, and create the tweet (and tweet it if it is different to the previous tweet) using: 

    make update


