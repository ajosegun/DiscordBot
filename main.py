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
bot = commands.Bot(command_prefix='!', help_command = help_command, description = 'Covid 19 Progress Visualization')

@bot.event
async def on_ready():
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

    # await bot.get_channel(guild.id).send("bot is online")


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
<<<<<<< HEAD
        "Records: Number of records to return",

        '1: Compare vaccination between 2 countries: !Compare Country1 Country2 Metrics Days',
        '2: Get countries with highest number of vaccinated people: !Top Records Metrics Days',
        '3: Get countries with lowest number of vaccinated people: !Bottom Records Metrics Days',
        '4: '
=======
        
        '1: Vaccination rate in a specific country: !See Country Metrics Days',
        '2: Compare vaccination between 2 countries: !Compare Country1 Country2 Metrics Days',
        '3: Get countries with highest number of vaccinated people: !Top Records Metrics Days',
        '4: Get countries with lowest number of vaccinated people: !Bottom Records Metrics Days',
        '5: Total Vaccinations Given in the World within given days: !World Metrics',
        '6: Total Vaccinations Given in the World within given days: !World_daily '
>>>>>>> a650a0e22e6ee04d85561f0fcfdbcf9d21923699
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


# @bot.event
# async def on_message(message):
    
#     ## Differientiate between messages from the bot and a user
#     if message.author == bot.user:
#         return

#     functions.log_message(message.content, bot.user.name)
#     print(message.content + " from " + bot.user.name)

#     if message.content in ["Hi", "Hello"]:
#         response = "Hello, welcome! How can I help you. Type !help"
        
#     # elif "help" in message.content.lower:
#     #     response = "Type !help or !help_me"
        
#     else:
#         response = "Sorry, I don't understand your message. Type !help for more information. "
    
#     await message.channel.send(response)

<<<<<<< HEAD
=======
@bot.command(name='World', help='Total Vaccinations Given in the World: Type !help_me')
async def world(ctx, metrics):
    '''
     Total Vaccinations Given in the World
    '''
    

    print( metrics)

    if metrics not in ["total_vaccinations"]:
        response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
        await ctx.send(response)
        return

    img_path = data_processing.total_vaccinations_given_in_world( metrics, bot.user.name)
    response = "Below is a world map showing the {}." .format(metrics)

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)


@bot.command(name='World_daily', help=' Daily vaccinations across the world: Type !help_me')
async def worldperc(ctx):
    '''
    Daily vaccinations
    '''
    

    img_path = data_processing.daily_vaccinated(bot.user.name)
    response = "Below is a world map showing the daily vaccinations."

    await ctx.send(response)
    await ctx.send(file=discord.File(img_path))
    functions.delete_file(img_path)


>>>>>>> a650a0e22e6ee04d85561f0fcfdbcf9d21923699
bot.run(TOKEN)

