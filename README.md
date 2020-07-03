# Twitter bot for Bristol, UK COVID-19 summary statistics

This repo contains a twitter bot to summarise daily COVID-19 statistics in Bristol, UK.

Data was drawn from: https://github.com/emmadoughty/Daily_COVID-19

As of 03 July 2020 data is drawn from the government website: https://coronavirus.data.gov.uk/

The code can easily be changed to summarise statistics from any UTLA in the UK by changing the Bristol code on line 50. 
To set up your own bot, you will need a set up access to the twitter API here: https://developer.twitter.com/en

To build the bot: 

Set up the environment and clone the data repository using:

    make install

Check for updates in the data repository, and create the tweet (and tweet it if it is different to the previous tweet) using: 

    make update


