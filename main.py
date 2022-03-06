import discord
import os
from alpha_vantage.foreignexchange import ForeignExchange
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


def get_exchange_rate(from_currency, to_currency):
    fe = ForeignExchange(key=str(os.getenv('ALPHAVANTAGE_API_KEY')))
    data, _ = fe.get_currency_exchange_rate(from_currency=from_currency,
                                            to_currency=to_currency)
    exchange_rate = round(float(data['5. Exchange Rate']), 2)
    return "{}/{} {}".format(from_currency, to_currency, exchange_rate)


@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + ' started')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(get_exchange_rate('USD', 'PLN')))


@bot.command(name="forex", brief="Provides given currency pair current exchange rate")
async def forex(ctx, arg):
    from_currency = str(arg)[0:3].upper()
    to_currency = str(arg)[3:6].upper()
    embed = discord.Embed(
        title=''
    )
    try:
        embed.description = get_exchange_rate(from_currency, to_currency)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Wystąpił błąd")


bot.run(os.getenv('TOKEN'))
