from sys import prefix
import discord
from discord.ext import commands, tasks
import random
import json 
import os 
import re

TOKEN = 'OTU1NjAxMDY4MTI4MTAwNDAz.G29eYX.bzypDwgeqTJVbpGQpnvvXTACx-_qV5gMrO6jcM'
client = discord.Client()
bannedWords = ["ban"]
bot = commands.Bot(command_prefix= prefix)
wl = []
#startup
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #get user info for each message
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    wl = user_message.split() 
    print(f'{username}:{user_message} ({channel})')

    if message.author == client.user:
        return 

    #test commands
    if message.channel.name == 'testing-commands':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello {username}!')
            return 
        elif user_message.lower() == 'bye':
            await message.channel.send("see you later " + username + "!")
            return 

    #server commands     
    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere!')
        return
    if (message.author.server_permissions.administrator): 
        if user_message.startswith('!bwa'):
            if len(wl) <= 2:     
                await message.channel.send(f'{wl[1]} has been banned. ')
        
            else: 
                await message.channel.send('Banned word must be a single word')
    
    
    def msg_contains_word(msg, word):
        return re.search(fr'\b({word})\b', msg) is not None 
    #ban messages
    if bannedWords != None and (isinstance(message.channel,     discord.channel.DMChannel) == False):
        for bannedWord in bannedWords:
            if msg_contains_word(user_message.lower(), bannedWord):
                await message.delete() 
                await message.channel.send(f"{message.author.mention} your message was removed as it contained a banned word")


    


    
            
client.run(TOKEN)
