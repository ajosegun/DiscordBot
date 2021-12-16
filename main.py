import pandas
import discord
import random
import matplotlib.pyplot as plt
import config

print("Starting Bot...")


TOKEN = config.TOKEN
GUILD = config.GUILD

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        #commented this line for test

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt. We are here again'
        ),
    ]

    if message.content == 'Hello':
        # response = random.choice(brooklyn_99_quotes)
        
        img = "grass.jpg"
        
        response = discord.File(img)

        await message.channel.send(file=discord.File(img))

        # await message.channel.send(response)

client.run(TOKEN)
