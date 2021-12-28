import discord
from discord.ext import commands
import config
import functions
import data_processing

print("Starting Bot...")

TOKEN = config.TOKEN
GUILD = config.GUILD

client = discord.Client()

help_command = commands.DefaultHelpCommand(
    no_category = 'Visualizations Commands'
)
bot = commands.Bot(command_prefix='!', help_command = help_command, description = 'Covid 19 Progress Visualization - Type !help')

@bot.event
async def on_ready():
    '''
    Bot start up activites
    '''
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
        await guild.text_channels[1].send("bot is online")

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    channel = bot.get_channel(config.channel_ID)
    await channel.send(f'{bot.user} is online:\nType !help or !help_me to get information on how to use me')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Aivancity Gamers server! Type Help to get started.'
    )


@bot.command(name='help_me', help='Provides information about the usage of this bot')
async def help_me(ctx):
    
    # description = "This bot shows information about the progress Covid 19 vaccinations around the world \n"
    help_messages = [
        "This bot shows information about the progress Covid 19 vaccinations around the world \n",
        "PLEASE READ CAREFULLY \n",
        "Metrics: total_vaccinations | total_vaccinations_per_hundred \n",
        "Days: 30 | 90 | 180 | 365 \n",
        "Country: The country name i.e France \n",
        "Records: Number of records to return",
        
        '1: Vaccination rate in a specific country: !See Country Metrics Days',
        '2: Compare vaccination between 2 countries: !Compare Country1 Country2 Metrics Days',
        '3: Get countries with highest number of vaccinated people: !Top Records Metrics Days',
        '4: Get countries with lowest number of vaccinated people: !Bottom Records Metrics Days',
        '5: Total Vaccinations Given in the World within given days: !World Metrics',
        '6: Total Vaccinations Given in the World within given days: !World_daily '
    ]

    response = "\n".join(help_messages)
    await ctx.send(response)

@bot.command(name='See', help='Vaccination rate in a specific country: Type !help_me')
async def vaccination_rate(ctx, country1, metrics, days: int):
    '''
     Vaccination rate in a specific country
    '''
    
    country_1 = country1.strip().title()

    print(country_1, metrics, days)

    if country_1 not in data_processing.country_list:
        response = "Country not found. Please check your entry again."
        await ctx.send(response)
        return

    if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
        response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
        await ctx.send(response)
        return

    img_path = data_processing.country_vaccination_rate(country_1, days, metrics, bot.user.name)
    response = "Below is a Line Plot showing the {} in {} within the last {} days." .format(metrics, country_1, days)

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)

@bot.command(name='Compare', help='Compare vaccination between 2 countries: Type !help_me')
async def compare(ctx, country1, country2, metrics, days: int):
    '''
     Compares vaccination between 2 countries
    '''
    
    country_1 = country1.strip().title()
    country_2 = country2.strip().title()

    print(country_1, country_2, metrics, days)

    if country_1 not in data_processing.country_list or country_2 not in data_processing.country_list:
        response = "Country not found. Please check your entry again."
        await ctx.send(response)
        return

    if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
        response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
        await ctx.send(response)
        return

    img_path = data_processing.compare_vaccinations_between_countries(country_1, country_2, days, metrics, bot.user.name)
    response = "Below is a Line Plot compaing the progress of {} between {} and {} within the last {} days." .format(metrics, country_1, country_2, days)

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)


@bot.command(name='Top', help='Get countries with the highest number of vaccinated people: Type !help_me')
async def top(ctx, records: int, metrics, days: int):
    '''
    Get countries with highest number of vaccinated people
    '''
    
    if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
        response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
        await ctx.send(response)
        return
    
    img_path = data_processing.get_top_bottom_vaccinated_countries("Top", records, days, metrics, bot.user.name)
    
    response = "Below is a Bar Chart showing the {} {} vaccinated countries within the last {} days." .format("Top", records, days)

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)

@bot.command(name='Bottom', help='Get countries with the lowest number of vaccinated people: Type !help_me')
async def bottom(ctx, records: int, metrics, days: int):
    '''
    Get countries with lowest number of vaccinated people
    '''
    
    if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
        response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
        await ctx.send(response)
        return
    
    img_path = data_processing.get_top_bottom_vaccinated_countries("Bottom", records, days, metrics, bot.user.name)
    
    response = "Below is a Bar Chart showing the {} {} vaccinated countries within the last {} days." .format("Bottom", records, days)

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)

@bot.command(name='World', help='Total Vaccinations Given in the World: Type !help_me')
async def world_total_vaccinations(ctx):
    '''
     Returns a vizualization of the total world vaccination as a map
    '''

    img_path = data_processing.total_vaccinations_given_in_world(bot.user.name)
    response = "Below is a world map showing the {}." .format("Total Vaccination")

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)

@bot.command(name='World_daily', help=' Daily vaccinations across the world: Type !help_me')
async def world_daily_vaccinations(ctx):
    '''
    Returns a vizualization of the world daily vaccination as a map
    '''

    img_path = data_processing.daily_vaccinated(bot.user.name)
    response = "Below is a world map showing the daily vaccinations."

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    '''
    A global error handler
    '''
    error_message = ""

    if isinstance(error, commands.errors.TooManyArguments):
        error_message = 'You have entered too many inputs. Type !help_me for more information'
        
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        error_message = 'Kindly enter all the required parameters. Type !help_me for more information'

    elif isinstance(error, commands.errors.CommandInvokeError):
        error_message = 'One of the parameters might be wrongly spelt. Type !help_me for more information'
    
    elif isinstance(error, commands.errors.ConversionError):
        error_message = 'Check one of the integer parameter you entered. Type !help_me to understand the commands to use'
        
    elif isinstance(error, commands.errors.UserInputError):
        error_message = 'Something about your input was wrong, please check your input and try again!'

    elif isinstance(error, commands.errors.CommandNotFound):
        error_message = "Sorry I don't understand your command. Type !help_me to understand the commands to use"
    
    else:
        error_message = 'Something went wrong! Type !help_me for more information or contact the administrator'

    await ctx.send(error_message + " \n" + str(error))

bot.run(TOKEN)

