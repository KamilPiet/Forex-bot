import discord
import asyncio
from alphavantage_api import *
from discord.ext import commands


# class CustomHelpCommand(commands.MinimalHelpCommand):
#    # !help
#    async def send_pages(self):
#        destination = self.get_destination()
#        for page in self.paginator.pages:
#            embed = discord.Embed(description=page)
#            await destination.send(embed=embed)
#
#
# bot = commands.Bot(command_prefix='!', help_command=CustomHelpCommand)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

auto_flag = False


def format_exchange_rate(from_currency, to_currency, exchange_rate, format_type):
    if format_type == 0:
        return "{}/{} {}".format(from_currency, to_currency, exchange_rate)
    elif format_type == 1:
        return "1 {} = {} {}".format(from_currency, exchange_rate, to_currency)
    else:
        return "{}/{} {}".format(from_currency, to_currency, exchange_rate)  # same as format_type = 0


@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + ' started')
    init_from_currency = 'USD'
    init_to_currency = 'PLN'
    exchange_rate = get_current_exchange_rate(init_from_currency, init_to_currency)
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(
                                  format_exchange_rate(init_from_currency, init_to_currency, exchange_rate, 0)))


@bot.command(name='now', brief="Provides the current exchange rate of the given currency pair")
# !forex
async def print_current_exchange_rate(ctx, arg):

    from_currency = str(arg)[0:3].upper()
    to_currency = str(arg)[3:6].upper()
    try:
        exchange_rate = get_current_exchange_rate(from_currency, to_currency)
        embed = discord.Embed(
            title='',
            colour=discord.Colour.green()
        )

        embed.description = "{} \n {}".format(format_exchange_rate(from_currency, to_currency, exchange_rate, 0),
                                              format_exchange_rate(from_currency, to_currency, exchange_rate, 1))
        await ctx.send(embed=embed)
    except:
        await ctx.send("Wystąpił błąd")


@bot.command(name='auto', brief="Toggle auto updating exchange rate in bot status",
             description="Current inverval is 1 minute")
# !auto
async def auto_update(ctx, arg):
    auto_from_currency = 'USD'
    auto_to_currency = 'PLN'
    interval = 300
    global auto_flag
    if bool(arg) != auto_flag:
        auto_flag = bool(arg)
        if auto_flag:
            await ctx.send("Włączono automatyczne odświeżanie kursu {}/{}".format(auto_from_currency, auto_to_currency))
        else:
            await ctx.send("Wyłączono automatyczne odświeżanie kursu")
    while auto_flag:
        await asyncio.sleep(interval)
        exchange_rate = get_current_exchange_rate(auto_from_currency, auto_to_currency)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(
                                  format_exchange_rate(auto_from_currency, auto_to_currency, exchange_rate, 0)))

bot.run(os.getenv('TOKEN'))
