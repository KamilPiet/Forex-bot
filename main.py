import discord
import os
from alpha_vantage.foreignexchange import ForeignExchange

client = discord.Client()


def get_exchange_rate(from_currency, to_currency):
    fe = ForeignExchange(key=str(os.getenv('ALPHAVANTAGE_API_KEY')))
    data, _ = fe.get_currency_exchange_rate(from_currency='USD', to_currency='PLN')
    return data


@client.event
async def on_ready():
    print('Bot {0.user} '.format(client) + ' started')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$usdpln'):
        await message.channel.send(str(get_exchange_rate('USD', 'PLN')))

client.run(os.getenv('TOKEN'))
