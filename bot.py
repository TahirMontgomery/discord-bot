import discord
import os
from io import BytesIO
import requests
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()

client = discord.Client()
cg = CoinGeckoAPI()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("!get"):
        coin_ticker = msg.split("-", 1)[1]

        coins = cg.get_coins()

        selected_coin = list(filter(lambda x: x["symbol"] == coin_ticker, coins))

        message_to_send = None
        if selected_coin:
            coin_name = selected_coin[0]["name"]
            usd_price = selected_coin[0]["market_data"]["current_price"]["usd"]

            line1 = f"You requested price information for {coin_name}.\n"
            line2 = "The current price in USD is ${:,.2f}".format(usd_price)

            message_to_send = line1 + line2
        else:
            message_to_send = "Could not find coin requested"

        await message.channel.send(message_to_send)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))
# coin_img = requests.get(
#     "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png?1547033579"
# )
# print(coin_img.text)
