from sys import prefix
import discord
from discord.ext import commands, tasks
import random
import re
import csv
from keep_alive import keep_alive
import os
from os import path

TOKEN = str(os.environ['DUE_TOKEN'])
client = discord.Client()
bot = commands.Bot(command_prefix=prefix)
wl = []
strikeCounters = 3


#startup
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(
        activity=discord.Game('https://discorduserenhancement.netlify.app/'))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        await channel.send(
            "Hello, my name is DUE! Please use !duehelp to learn about my commands!"
        )
        break


@client.event
async def on_message_edit(before, after):
    username = str(after.author).lower().split('#')[0]
    username = removechar(username)
    usernameReal = str(after.author).lower()
    user_message = str(after.content)

    serverID = after.guild.id
    bannedWordsList = []
    names = []
    strikes = []
    global serverFileBannedList
    serverFileBannedList = "/home/runner/DUE-2/bannedlists/" + " " + str(
        serverID) + ' bannedList.csv'
    print(serverFileBannedList)
    global serverFileStrikeList
    serverFileStrikeList = "/home/runner/DUE-2/strike/" + " " + str(
        serverID) + ' StrikeCount.csv'
    global serverFileStrikeCounter
    serverFileStrikeCounter = "/home/runner/DUE-2/strikecounter/" + " " + str(
        serverID) + ' StrikeCounter.csv'
    global serverFileChannelType
    serverFileChannelType = "/home/runner/DUE-2/channeltypes/" + " " + ' channeltype.csv'
    print("Test")
    with open(serverFileBannedList) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            bannedWordsList.append(str(row[0]))

    with open(serverFileStrikeList, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                names.append(str(row[0]))
                strikes.append(int(row[1]))
            except:
                continue

    if bannedWordsList != None and (isinstance(
            after.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWordsList:
            if msg_contains_word(user_message.lower(), bannedWord):
                try:
                    await after.delete()
                except:
                    None
                await after.channel.send(
                    f"{after.author.mention} your message was removed as it contained a banned word"
                )
                try:
                    with open(serverFileStrikeCounter, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            strikeCounter = int(row[0])
                    strike(usernameReal.lower())
                    if strikes[names.index(usernameReal)] >= strikeCounter:
                        print(strikeCounter)
                        print("test sucess")
                        await after.channel.send(
                            f'{username} has exceeded maximum strikes')
                except:
                    print(strikeCounter)
                    print("fail")
                    None


@client.event
async def on_message(message):
    global strikeCounters
    serverID = message.guild.id
    bannedWordsList = []
    names = []
    strikes = []
    global serverFileBannedList
    serverFileBannedList = "/home/runner/DUE-2/bannedlists/" + " " + str(
        serverID) + ' bannedList.csv'
    print(serverFileBannedList)
    global serverFileStrikeList
    serverFileStrikeList = "/home/runner/DUE-2/strike/" + " " + str(
        serverID) + ' StrikeCount.csv'
    global serverFileStrikeCounter
    serverFileStrikeCounter = "/home/runner/DUE-2/strikecounter/" + " " + str(
        serverID) + ' StrikeCounter.csv'
    global serverFileChannelType
    serverFileChannelType = "/home/runner/DUE-2/channeltypes/" + " " + str(
        serverID) + ' channeltype.csv'
    global serverFileBannedWordsInList
    serverFilerBannedWordsInList = "/home/runner/DUE-2/" + " " + 'bannedWordsInList.csv'
    if not (path.exists(serverFileBannedList)) and not (
            path.exists(serverFileStrikeList)) and not (
                path.exists(serverFileStrikeCounter)) and not (
                    path.exists(serverFileChannelType)):

        open(serverFileBannedList, 'x')
        open(serverFileStrikeList, 'x')
        open(serverFileStrikeCounter, 'x')
        open(serverFileChannelType, 'x')
        open(serverFileBannedWordsInList, 'x')

        with open(serverFileStrikeCounter, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(str(strikeCounters))

    #get user info for each message
    username = str(message.author).lower().split('#')[0]
    username = removechar(username)
    usernameReal = str(message.author).lower()
    usernameReal = removechar(usernameReal)

    print(username)
    user_message = str(message.content)
    channel = str(message.channel.name)
    wl = user_message.lower().split()
    print(f'{username}:{user_message} ({channel})')
    if message.author == client.user:
        return

    #check what type the message sent is
    filetype = []

    if len(wl) >= 1:
        str(user_message)
        filetype.append("text")
        print("test")

    formats = ['jpg', 'gif', 'svg', "png", 'jpeg']
    attachments = [
        f for f in message.attachments
        if f.filename.lower().split('.')[-1] in formats
    ]
    if message.channel.name == channel and attachments:
        filetype.append("image")

    snd = [
        "wav", "pcm", "3gp", "aa", "aac", "aax", "act", "aiff", "alac", "amr",
        "ape", "au", "awb", "dss", "dvf", "flac", "gsm", "iklax", "ivs", "m4a",
        "m4b", "m4p", "mmf", "mp3", "mpc", "msv", "nmf", "ogg", "oga", "mogg",
        "opus", "ra,", "rm", "raw", "rf64", "sln", "tta", "voc", "vox", "wma",
        "webm", "8svx", "cda"
    ]

    attachments2 = [
        f for f in message.attachments
        if f.filename.lower().split('.')[-1] in snd
    ]
    if message.channel.name == channel and attachments2:
        filetype.append("sound")

    video = [
        "WEBM", "MPG", "MP2", "MPEG", "MPE", "MPV", "OGG", "MP4", "M4P", "M4V",
        "AVI", "WMV", "MOV", "QT", "FLV", "SWF", "AVCHD"
    ]

    attachments3 = [
        f for f in message.attachments
        if f.filename.upper().split('.')[-1] in video
    ]
    if message.channel.name == channel and attachments3:
        filetype.append("video")

    if str(message.content).startswith("http://") or str(
            message.content).startswith("https://"):
        filetype.append("link")

    try:
        if message.embeds != []:
            filetype.append("embed")
    except:
        None

    if len(filetype) <= 0:
        filetype.append("file")

    ServerFileList = []
    rowies = []
    allowed = ["embed", "text", "sound", "file", "video", "link", "image"]

    with open(serverFileChannelType) as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            ServerFileList.append(row[0])
            rowies.append(row[1:])
    if channel in ServerFileList:
        allowed = rowies[ServerFileList.index(channel)]
        #implement logic that adds all the proper
    for i in filetype:
        if i not in allowed:
            try:
                await message.delete()
            except:
                None
            break
    #help
    if user_message.lower() == "!duehelp":
        await message.channel.send(
            '**List Of Commands:**' +
            "\n \n ***BASIC:***```!hello - DUE says hello \n!bye - DUE says bye \n!strikes (username_without_spaces#XXXX) - Lists amount of strikes user has ```\n ***ADMIN:*** ```\n !bwa (single_word) - Adds word to banned word list \n !bwr (single_word) - Removes word from banned word list \n !bwc - Clears all words from banned word list \n !bwv - View the words in the banned word list \n !clearallstrikes - Clears all strikes for all users \n !clearstrikes (username_without_spaces#XXXX) - Clears strikes of the username \n !setstrike (int) - Sets minimum number of strikes to get a warning \n !channeladd (link, text, image, video, embed, sound, file) - Allows this type of message in a channel \n !channelremove (link, text, image, video, embed, sound, file) - Bans the message type from being in the channel \n !channeldisplay - Displays what message type(s) is allowed in a channel ```\n ***IMPORTANT NOTES:*** ```Usernames must have no spaces and have their 4 digit tag \nBanned words must be a single word \nDuplicate channel names will not work \nAll other message types not listed above are classified as files\nDefault strike warning value is 3\nA channel will automatically allow all filetypes \nYou can only add/remove one message type at a time```"
        )
    #test commands
    if user_message.lower() == '!hello':
        await message.channel.send(f'Hello {username}!')
        return
    elif user_message.lower() == '!bye':
        await message.channel.send("see you later " + username + "!")
        return

    with open(serverFileBannedList) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            bannedWordsList.append(str(row[0]))

    with open(serverFileStrikeList, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                names.append(str(row[0]))
                strikes.append(int(row[1]))
            except:
                continue

#Add word to banned word list
    if user_message.startswith('!bwa') and (
            message.author.guild_permissions.administrator):
        rows = []
        if len(wl) == 2:
            if wl[1] not in bannedWordsList:
                with open(serverFileBannedList, 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow({wl[1]})
                    bannedWordsList.append(wl[1])
                await message.channel.send("Word banned")
            else:
                await message.channel.send(
                    'Banned word must not already be in the list')
    ########################################################
            with open(serverFilerBannedWordsInList, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow({wl[1]})
                bannedWordsList.append(wl[1])
        else:
            await message.channel.send('Banned word must be a single word')
    elif user_message.startswith('!bwa') and (
            message.author.guild_permissions.administrator == False):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )

    #clear banned words list
    if user_message.startswith('!bwc') and (
            message.author.guild_permissions.administrator):
        rows = []
        with open(serverFileBannedList, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    elif user_message.startswith('!bwc') and (
            message.author.guild_permissions.administrator == False):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )

    #remove word from banned word list
    if user_message.startswith('!bwr') and (
            message.author.guild_permissions.administrator):
        if len(wl) == 2:
            if wl[1] in bannedWordsList:
                rows = []
                with open(serverFileBannedList, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        rows.append(row)
                    for i in rows:
                        if i == [wl[1]]:
                            rows.remove(i)
                with open(serverFileBannedList, 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)
                print(bannedWordsList)
                bannedWordsList.remove(wl[1])
                await message.channel.send('Word removed')
            else:
                await message.channel.send(
                    'Banned word is not in list or command was used incorrectly'
                )
        else:
            await message.channel.send('Banned word must be a single word')
    elif user_message.startswith('!bwr') and (
            message.author.guild_permissions.administrator == False):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )
    #let user view banned word list
    if user_message.startswith('!bwv') and (
            message.author.guild_permissions.administrator) and len(wl) == 1:
        rows = []
        with open(serverFileBannedList, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row[0])
        if len(rows) > 2:
            await message.channel.send(
                f'The banned words are {", ".join(rows[:-1])}' + ', and ' +
                rows[-1])
        elif len(rows) == 2:
            await message.channel.send(f'The banned words are ' + rows[0] +
                                       ' and ' + rows[1])
        elif len(rows) == 1:
            await message.channel.send(f'The only banned word is ' + rows[0])
        elif len(rows) == 0:
            await message.channel.send(f"The banned words list is empty.")
    elif len(wl) != 1 and (message.author.guild_permissions.administrator
                           ) and user_message.startswith('!bwv'):
        await message.channel.send("Command was used incorrectly")

    elif user_message.startswith('!bwv') and not (
            message.author.guild_permissions.administrator):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )
    #let user see the amount of strikes they have
    if user_message.startswith('!strikes') and len(wl) == 2:
        strikes = 0
        rows = []
        if wl[1] in names:
            with open(serverFileStrikeList, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if str(row[0]) == wl[1]:
                        strikes += int(row[1])
                        if usernameReal == wl[1]:
                            if strikes == 1:
                                await message.channel.send(
                                    f"{message.author.mention} you have " +
                                    f'{strikes}' + " strike")
                            else:
                                await message.channel.send(
                                    f"{message.author.mention} you have " +
                                    f'{strikes}' + " strikes")
                        else:
                            if strikes != 1:
                                await message.channel.send(wl[1] + " has " +
                                                           f'{strikes}' +
                                                           " strikes")
                            else:
                                await message.channel.send(wl[1] + " has " +
                                                           f'{strikes}' +
                                                           " strike")
        else:
            await message.channel.send('Username does not have any strikes')
    elif user_message.startswith('!strikes'):
        await message.channel.send("Command used incorrectly")

    #clear all strikes
    if (user_message.startswith('!clearallstrikes')) and (
            message.author.guild_permissions.administrator):
        rows = []
        with open(serverFileStrikeList, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    elif user_message.startswith('!clearallstrikes') and (
            message.author.guild_permissions.administrator == False):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )

    #clear strikes for a certain user
    if user_message.startswith('!clearstrikes') and (
            message.author.guild_permissions.administrator):
        if len(wl) == 2:
            if wl[1] in names:
                rows = []
                with open(serverFileStrikeList, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        rows.append(row)
                    for i in rows:
                        if i[0] == wl[1]:
                            rows.remove(i)
                with open(serverFileStrikeList, 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)
                names.remove(wl[1])
                print(wl[1])
                print(username)
                if username == wl[1]:
                    await message.channel.send(
                        f"{message.author.mention} your strikes are cleared")
                else:
                    await message.channel.send(wl[1] +
                                               "'s strikes are cleared")
            else:
                await message.channel.send(
                    'Person has no strikes or command was used incorrectly')
        else:
            await message.channel.send('Name must be a single word')
    elif user_message.startswith('!clearstrikes') and (
            message.author.guild_permissions.administrator == False):

        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )

    #setstrike
    if user_message.startswith('!setstrike') and (
            message.author.guild_permissions.administrator) and len(wl) == 2:
        with open(serverFileStrikeCounter, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                strikeCounter = int(row[0])
        try:
            if (isinstance(int(wl[1]), int)):
                strikeCounter = int(wl[1])
                print("Success " + str(strikeCounter))
                with open(serverFileStrikeCounter, 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(str(strikeCounter))
        except:
            await message.channel.send("Value passed must be an integer")
    elif user_message.startswith('!setstrike') and not (
            message.author.guild_permissions.administrator):
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )
    elif user_message.startswith('!setstrike') and (
            message.author.guild_permissions.administrator) and len(wl) != 2:
        await message.channel.send("Must be a single number passed")

#secretCommand For Data
    if user_message.startswith('!datadatadata'):
        data = []

        with open(serverFilerBannedWordsInList) as csvDataFile:

            csvReader = csv.reader(csvDataFile)

            for row in csvReader:
                data.append(row[0])

        print(create_word_count_array(data))

    #ban messages
    if bannedWordsList != None and (isinstance(
            message.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWordsList:
            if msg_contains_word(user_message.lower(), bannedWord):
                try:
                    await message.delete()

                except:
                    await message.channel.send(
                        f"{message.author.mention} your message was removed as it contained a banned word"
                    )
                if user_message.startswith('!bwa'):
                    break
                else:
                    try:
                        with open(serverFileStrikeCounter, 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for row in reader:
                                strikeCounter = int(row[0])
                        strike(usernameReal.lower())
                        if strikes[names.index(usernameReal)] >= strikeCounter:
                            print(strikeCounter)
                            print("test sucess")
                            await message.channel.send(
                                f'{username} has exceeded maximum strikes')
                    except:
                        print(strikeCounter)
                        print("fail")
                        None
    #file specific channel
    if user_message.startswith('!channeladd') and (
            message.author.guild_permissions.administrator) and len(wl) == 2:
        channelhas = [
            "image", "text", "video", "sound", 'link', 'file', 'embed'
        ]
        if wl[1] in channelhas:
            #Write to channeltype file with the first column being the channel name, and the second column being the file type allowed in the server
            channelnames = []
            rows = []
            with open(serverFileChannelType, "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    try:
                        channelnames.append(row[0])
                        rows.append(row)
                    except:
                        None
            if channel not in channelnames:
                rows.append([channel])
                channelnames.append(channel)
                for i in channelhas:
                    rows[-1].append(i)
            if channel in channelnames:
                if wl[1] in rows[channelnames.index(channel)]:
                    print('this is already a channel type of this channel')
                    await message.channel.send(
                        "This is already a channel type of this channel")
                else:
                    rows[channelnames.index(channel)].append(wl[1])
            with open(serverFileChannelType, "w") as csvfiles:
                writer = csv.writer(csvfiles)
                writer.writerows(rows)
            print(
                f'{channel} allows {", ".join(rows[channelnames.index(channel)][1:])}'
            )
        if len(rows[channelnames.index(channel)]) > 3:
            await message.channel.send(
                f'This channel allows {"s, ".join(rows[channelnames.index(channel)][1:-1])}'
                + 's, and ' + rows[channelnames.index(channel)][-1] + 's')
        elif len(rows[channelnames.index(channel)]) == 3:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's and ' + rows[channelnames.index(channel)][2] + 's')
        elif len(rows[channelnames.index(channel)]) == 2:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's')
        elif len(rows[channelnames.index(channel)]) == 1:
            await message.channel.send(
                f"This channel doesn't allow any messages.")

    elif user_message.startswith('!channeladd') and len(wl) == 2:
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )
    elif user_message.startswith('!channeladd'):
        await message.channel.send("Command used incorrectly")

    if user_message.startswith('!channelremove') and (
            message.author.guild_permissions.administrator) and len(wl) == 2:
        rows = []
        channelnames = []
        channelhas = [
            "image", "text", "video", "sound", 'link', 'file', 'embed'
        ]
        with open(serverFileChannelType, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                try:
                    channelnames.append(row[0])
                    rows.append(row)
                except:
                    None
            if channel not in channelnames:
                rows.append([channel])
                channelnames.append(channel)
                for i in channelhas:
                    rows[-1].append(i)
            if channel in channelnames:
                if wl[1] in channelhas:
                    if wl[1] in rows[channelnames.index(channel)]:
                        rows[channelnames.index(channel)].remove(wl[1])
                        with open(serverFileChannelType, "w") as csvfiles:
                            writer = csv.writer(csvfiles)
                            writer.writerows(rows)
                    else:
                        await message.channel.send(
                            'This has already been removed')
                else:
                    await message.channel.send(
                        'This isnt a proper channel type')
        print(
            f'{channel} allows {", ".join(rows[channelnames.index(channel)][1:])}'
        )
        if len(rows[channelnames.index(channel)]) > 3:
            await message.channel.send(
                f'This channel allows {"s, ".join(rows[channelnames.index(channel)][1:-1])}'
                + 's, and ' + rows[channelnames.index(channel)][-1] + 's')
        elif len(rows[channelnames.index(channel)]) == 3:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's and ' + rows[channelnames.index(channel)][2] + 's')
        elif len(rows[channelnames.index(channel)]) == 2:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's')
        elif len(rows[channelnames.index(channel)]) == 1:
            await message.channel.send(
                f"This channel doesn't allow any messages.")
    elif user_message.startswith('!channelremove') and len(wl) == 2:
        await message.channel.send(
            f"{message.author.mention} you must have admin permissions to use this command"
        )
    elif user_message.startswith('!channelremove'):
        await message.channel.send("Command used incorrectly")

    print(filetype)

    if user_message.startswith('!channeldisplay') and (
            message.author.guild_permissions.administrator) and len(wl) == 1:
        rows = []
        channelnames = []
        channelhas = [
            "image", "text", "video", "sound", 'link', 'file', 'embed'
        ]
        with open(serverFileChannelType, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                try:
                    channelnames.append(row[0])
                    rows.append(row)
                except:
                    None
            if channel not in channelnames:
                rows.append([channel])
                channelnames.append(channel)
                for i in channelhas:
                    rows[-1].append(i)
        with open(serverFileChannelType, "w") as csvfiles:
            writer = csv.writer(csvfiles)
            writer.writerows(rows)
        if len(rows[channelnames.index(channel)]) > 3:
            await message.channel.send(
                f'This channel allows {"s, ".join(rows[channelnames.index(channel)][1:-1])}'
                + 's, and ' + rows[channelnames.index(channel)][-1] + 's')
        elif len(rows[channelnames.index(channel)]) == 3:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's and ' + rows[channelnames.index(channel)][2] + 's')
        elif len(rows[channelnames.index(channel)]) == 2:
            await message.channel.send(
                f'This channel allows {rows[channelnames.index(channel)][1]}' +
                's')
        elif len(rows[channelnames.index(channel)]) == 1:
            await message.channel.send(
                f"This channel doesn't allow any messages.")


#functions
def msg_contains_word(msg, word):
    msg = removechar(msg)
    if word in msg:
        return True
    else:
        return False


def strike(name):
    with open(serverFileStrikeList) as csvfile:
        rows = []
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            rows.append(row)
        for i in rows:
            try:
                if i[0] == name:
                    i[1] = int(i[1]) + 1
                    with open(serverFileStrikeList, 'w') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerows(rows)
                    return
            except:
                continue
        with open(serverFileStrikeList, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([name, 1])


def removechar(string):
    return string.replace(" ", "")

def create_word_count_array(words):
  freqmap = {}
  for i in words:
    if i not in freqmap.keys():
      freqmap[i] = 1
    else:
      freqmap[i] += 1
  return freqmap

keep_alive()
client.run(TOKEN)
