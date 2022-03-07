import discord
import os
import asyncio
from alpha_vantage.foreignexchange import ForeignExchange
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super.__init__()

    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)


bot = commands.Bot(command_prefix='!', help_command=CustomHelpCommand)

auto_flag = False


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
        title='',
        colour=discord.Colour.green()
    )
    try:
        embed.description = get_exchange_rate(from_currency, to_currency)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Wystąpił błąd")


@bot.command(name="auto", brief="Turn on or off autoupdating exchange rate in bot status")
async def auto(ctx, arg):
    global auto_flag
    if bool(arg) != auto_flag:
        auto_flag = bool(arg)
    while auto_flag:
        await asyncio.sleep(2)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(get_exchange_rate('BTC', 'USD')))

bot.run(os.getenv('TOKEN'))
