import discord
import asyncio
from alphavantage_api import *
from discord.ext import commands, tasks


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
auto_from_currency = 'USD'
auto_to_currency = 'PLN'


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
    await bot.change_presence(status=discord.Status.do_not_disturb)
    update_exchange_rate.start()


@bot.command(name='now', brief="Provides the current exchange rate of the given currency pair",
             description="Provides the current exchange rate of the given currency pair.\n"
                         "Example: !now usdpln")
# !now
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
             description="Toggle auto updating exchange rate in bot status.\n"
                         "Current inverval is 1 hour.\n"
                         "Example:\n"
                         "!auto on\n"
                         "!auto off")
# !auto
async def auto_update(ctx, arg):
    global auto_flag
    if arg in ["True", "true", "on", "1"]:
        arg_bool = True
    else:
        arg_bool = False
    if arg_bool != auto_flag:
        auto_flag = arg_bool
        if auto_flag:
            await ctx.send("Włączono automatyczne odświeżanie kursu")
            exchange_rate = get_current_exchange_rate(auto_from_currency, auto_to_currency)
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(
                format_exchange_rate(auto_from_currency, auto_to_currency, exchange_rate, 0)))
        else:
            await ctx.send("Wyłączono automatyczne odświeżanie kursu")
            await bot.change_presence(status=discord.Status.do_not_disturb)


@tasks.loop(minutes=15)
async def update_exchange_rate():
    if auto_flag:
        exchange_rate = get_current_exchange_rate(auto_from_currency, auto_to_currency)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(
            format_exchange_rate(auto_from_currency, auto_to_currency, exchange_rate, 0)))


bot.run(os.getenv('TOKEN'))
