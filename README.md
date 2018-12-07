# @FastTweetBot

A Telegram bot that helps you update your Twitter status without having to
access Twitter. This is a personalised bot as the bot is only allowed to post
on behalf of the bot owner.

This application is powered by [tweepy](https://github.com/tweepy/tweepy) and
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Setting up

We assume that you already have created a Twitter developer account and have
talked to the BotFather.

1. Make sure that you have **Python 3**, **pip** and **Python virtual environment** installed
2. Run the following commands
  ```shell
  $ git clone https://github.com/CT15/FastTweetBot.git
  $ cd FastTweetBot
  ```
3. Create and activate python3 virtual environment
  ```shell
  $ python3 -m venv venv
  $ source venv/bin/activate # Make sure that `python --version` is 3.x.x
  ```
4. Install dependencies
  ```shell
  $ pip install -r requirements.txt
  ```
5. Run `./setup.sh`
6. Fill in the necessary details in `keys_tokens.py` and `telegram_id.py` files
7. Run the `python bot.py` (run this continuously from a server to permanently enable your bot)

You can deactivate python3 virtual environment by running `deactivate`. Note
that your program will not run without the virtual environment activated.

## License
This project is available under the MIT license. See the LICENSE file for more info.
