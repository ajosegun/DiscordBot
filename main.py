import pandas
import discord
import random

import config
import functions
import os
import data_processing


print("Starting Bot...")

TOKEN = config.TOKEN
GUILD = config.GUILD

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Aivancity Gamers server! Type Help to get started.'
    )

@client.event
async def on_message(message):
    
    ## Differientiate between messages from the bot and a user
    if message.author == client.user:
        return

    functions.log_message(message.content, client.user.name)

    print(message.content + " from " + client.user.name)

    if 'help' in message.content.lower():
        # description = "This bot shows information about the progress Covid 19 vaccinations around the world \n"
        help_messages = [
            "This bot shows information about the progress Covid 19 vaccinations around the world \n",
            "PLEASE READ CAREFULLY \n",
            "Metrics: total_vaccinations | total_vaccinations_per_hundred \n",
            "Days: 30 | 90 | 180 | 365 \n",
            "Country: The country name i.e France \n",

            '1: Compare vaccination between 2 countries: Type exactly this format: 101 - Country1 - Country2 - Metrics - Days',
            '2: To see countries with highest/lowest number of vaccinated people: 102 - Top (or Bottom) - 10 - Metrics - Days',
            '3: '
            
        ]

        response = "\n".join(help_messages)

        await message.channel.send(response)
    elif '101' in message.content.lower():
        country_1 = ""
        country_2 = ""
        days = ""
        metrics = ""

        the_user_message = message.content.lower().split("-")
        if len(the_user_message) > 3:
            country_1 = the_user_message[1].strip().capitalize()
            country_2 = the_user_message[2].strip().capitalize()
            metrics = the_user_message[3].strip().lower()
            days = the_user_message[4].strip()
        else:
            response = "There is an issue with your entry, please try again or type help."
            await message.channel.send(response)
            return

        if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
            response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
            await message.channel.send(response)
            return

        try:
            days = int(days) 
        except Exception as e:
            response = "Check the input again. Days need to be a number"
            await message.channel.send(response)
            functions.error_log("Input: " + str(e))
            return


        img_path = data_processing.compare_vaccinations_between_countries(country_1, country_2, days, metrics, client.user.name)
        

        response = "You selected 101 \n\n Below is a Line Plot compaing the progress of {} between {} and {} with the last {} days." .format(metrics, country_1, country_2, days)

        await message.channel.send(response)
        await message.channel.send(file=discord.File(img_path))

        functions.delete_file(img_path)
    
    elif '102' in message.content.lower():
        top_bottom = ""        
        number_of_records = ""
        metrics = ""
        days = ""

        the_user_message = message.content.lower().split("-")

        if len(the_user_message) > 3:
            top_bottom = the_user_message[1].strip().capitalize()
            number_of_records = the_user_message[2].strip().capitalize()
            metrics = the_user_message[3].strip().lower()
            days = the_user_message[4].strip()
        else:
            response = "There is an issue with your entry, please try again or type help."
            await message.channel.send(response)
            return

        if metrics not in ["total_vaccinations", "total_vaccinations_per_hundred"]:
            response = "Check the input again. Metrics need to be either total_vaccinations or total_vaccinations_per_hundred"
            await message.channel.send(response)
            return
        
        try:
            number_of_records = int(number_of_records) 
            days = int(days) 
        except Exception as e:
            response = "Check the input again. Number of records or days need to be numbers"
            await message.channel.send(response)
            functions.error_log("Input" + str(e))
            return
        
        img_path = data_processing.get_top_bottom_vaccinated_countries(top_bottom, number_of_records, days, metrics, client.user.name)
        
        response = "You selected 102 \n\n Below is a Bar Chart showing the {} {} vacinnated countries with the last {} days." .format(top_bottom, number_of_records, days)

        await message.channel.send(response)
        await message.channel.send(file=discord.File(img_path))

        functions.delete_file(img_path)

    elif message.content == 'raise-exception':
        raise discord.DiscordException

    else:
        response = "Sorry, I don't understand your message. Type help for more information. "

        await message.channel.send(response)


client.run(TOKEN)
