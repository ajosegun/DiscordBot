import pandas
import discord
import random
import matplotlib.pyplot as plt

print("Starting Bot...")


TOKEN = "OTE4MTY2ODUwNTc0MTE4OTgz.YbDTgw.Vplms-ToVFbl8h7VmNUkcnShMX4"
GUILD = "PGE2 ADAV"

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

    if message.content == 'Hi':
        # response = random.choice(brooklyn_99_quotes)
        
        img = "grass.jpg"
        
        response = discord.File(img)

        await message.channel.send(file=discord.File(img))

        # await message.channel.send(response)

client.run(TOKEN)
