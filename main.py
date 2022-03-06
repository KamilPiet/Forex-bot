import discord
import os
from alpha_vantage.foreignexchange import ForeignExchange

client = discord.Client()


def get_exchange_rate(from_currency, to_currency):
    fe = ForeignExchange(key=str(os.getenv('ALPHAVANTAGE_API_KEY')))
    data, _ = fe.get_currency_exchange_rate(from_currency=from_currency,
                                            to_currency=to_currency)
    exchange_rate = round(float(data['5. Exchange Rate']), 2)
    return exchange_rate


@client.event
async def on_ready():
    print('Bot {0.user} '.format(client) + ' started')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('USD/PLN '+str(get_exchange_rate('USD', 'PLN'))))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        from_currency = str(message.content)[1:4].upper()
        to_currency = str(message.content)[4:7].upper()
        await message.channel.send(str(get_exchange_rate(from_currency, to_currency)))

client.run(os.getenv('TOKEN'))
