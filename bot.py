import discord
import asyncio

import timeutils

import datetime
import pytz
import json

import requests

import random

client = discord.Client()

fo = open("settings.json")
settings = json.load(fo)
fo.close()

TIG_ID = "291451818712629249"
KINGS_ID = "305438956701614081"

time_format = "%y/%m/%d [%H:%M:%S]"

# TODO: Organize this sanely

def log_event(message):
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] "
    + message)


@client.event
async def on_server_join(server):
    log_event("Joined server " + server.name)
    settings[server.id] = {}
    fo = open("settings.json", "w+")
    json.dump(settings, fo)
    fo.close()
    log_event("Settings has been updated")

@client.event
async def on_ready():
    log_event("logged in as:\n %s\n %s\n-------" % (client.user.name, client.user.id))

@client.event
async def on_message(message):
    #TODO: Create a handler for these, rather than doing this
    global time_format

    if message.content.startswith("!test"):
        if not is_enabled_channel(message):
            await client.send_message(message.channel,
                                      "This channel is not enabled. Please have an administrator run !enable")
            return
        if message.author.id == TIG_ID:
            await client.send_message(message.channel, "eyy bb ;)")
        elif message.author.id == KINGS_ID:
            await client.send_message(message.channel, ":crown: All Hail " + message.author.mention + "! :crown:")
        else:
            await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.startswith("!time"):
        if not is_enabled_channel(message):
            await client.send_message(message.channel,
                                      "This channel is not enabled. Please have an administrator run !enable")
            return
        tokenized = message.content.split()

        if (len(tokenized) > 1):
            try:
                #this should be a timezone
                #hopefully
                timestr = message.author.mention + ", the current time in " \
                          + tokenized[1]  + " is `" \
                          + timeutils.current_time_for_timezone(tokenized[1], time_format) + "`"
            except:
                timestr = "That timezone is unsupported."
            
        else:
            stringtime = timeutils.current_utc_time(time_format)
            timestr = message.author.mention + ", the current time is `" + stringtime + "`"
            
        await client.send_message(message.channel, timestr)

    elif message.content.startswith("!tigtime"):
        if not is_enabled_channel(message):
            await client.send_message(message.channel,
                                      "This channel is not enabled. Please have an administrator run !enable")
            return
        au = pytz.timezone("Australia/Sydney")
        stringtime = timeutils.current_time_for_timezone(au, time_format)

        await client.send_message(message.channel, "it is `" + stringtime + "` for tigrriis")

    elif message.content.startswith("!kingstime"):
        if not is_enabled_channel(message):
            await client.send_message(message.channel,
                                      "This channel is not enabled. Please have an administrator run !enable")
            return
        ut = pytz.timezone("US/Mountain")
        stringtime = timeutils.current_time_for_timezone(ut, time_format)

        await client.send_message(message.channel, "it is `" + stringtime + "` for jkings")


    elif message.content.startswith("!quote"):
        await client.send_message(message.channel, get_random_quote())

    elif message.content.startswith("!disable"):
        if (not message.author.permissions_in(message.channel).administrator):
            await client.send_message(message.channel, "Please have an administrator run this command")

        if message.channel.name in settings[message.server.id]["enabledChannels"]:
            settings[message.server.id]["enabledChannels"].remove(message.channel.name)

            fo = open("settings.json", "w+")
            json.dump(settings, fo)
            fo.close()
            log_event("Settings updated for server " + message.server.name)

            await client.send_message(message.channel, "This channel is no longer enabled")


    elif message.content.startswith("!help"):
        splitmessage = message.content.split()
        if len(splitmessage) > 1 and splitmessage[1] == "time":
            await client.send_message(message.channel,
                                      "For a list of supported timezones, please see " +
                                      "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
        else:
            fo = open("help.txt")
            content = fo.read()

            await client.send_message(message.channel, content)
            fo.close()

    elif message.content.startswith("!enable"):
        if message.author.permissions_in(message.channel).administrator:
            try:
                if (message.channel.name) not in (settings[message.server.id]["enabledChannels"]):
                    settings[message.server.id]["enabledChannels"].append(message.channel.name)
                    message_string = "This channel has been added to your Enabled Channels!"
                else:
                    message_string = "This channel has already been added to your active channels"
            except KeyError:
                settings[message.server.id]["enabledChannels"] = [message.channel.name]
                message_string = "This channel has been added to your Enabled Channels!"

            fo = open("settings.json", "w+")
            json.dump(settings, fo)
            fo.close()
            log_event("Settings updated for " + message.server.name)


            await client.send_message(message.channel, message_string)

        else:
            await client.send_message(message.channel,
                                "You do not have permission to activate this channel. " +
                                      "Please have an administrator run !enable")

    elif message.content.startswith("!gay"):
        if not is_enabled_channel(message):
            await client.send_message(message.channel,
                                      "This channel is not enabled. Please have an administrator run !enable")
            return

        gayness = ["gaaaaaay", "yes", "very", "indeed", "of course", "sure why not", "unbelievably so",
                   "only for tigrriis", "only for jkings", "oh you just noticed?", "pfft", ":wink:", ":kissing_heart:",
                   ":gay_pride_flag:", ":eggplant:"]
        await client.send_message(message.channel, random.choice(gayness))

@client.event
async def on_member_update(before, after):
    log_event(before.name + "'s status has changed")
    if before.id == KINGS_ID:
        if before.status == discord.Status.offline and not after.status == discord.Status.offline:
            user = await client.get_user_info(KINGS_ID)
            log_event(user.name)
            await client.send_message(user, "Hey, you're online!")

    if before.id == TIG_ID:
        if before.status == discord.Status.offline and not after.status == discord.Status.offline:
            user = await client.get_user_info(KINGS_ID)
            await client.send_message(user, "Your boyfriend is online.")
            await client.send_message(before, "Hey bb ;)")

    if len(after.roles) > len(before.roles):
        enabled_channels = []
        for channel in before.server.channels:
            if channel.name in settings[before.server.id]["enabledChannels"]:
                enabled_channels.append(channel)

        for channel in enabled_channels:
            await client.send_message(channel, before.name + " just gained a new role!")

    elif len(before.roles) > len(after.roles):
        enabled_channels = []
        for channel in before.server.channels:
            if channel.name in settings[before.server.id]["enabledChannels"]:
                enabled_channels.append(channel)

        for channel in enabled_channels:
            await client.send_message(channel, before.name + " just lost a role! lol.")

def get_random_quote():
    quote = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
    quote = json.loads(quote.text)

    message = "\"" + quote["quoteText"] + "\""
    message += "\n\n -- " + quote["quoteAuthor"]

    return message

def is_enabled_channel(message):
    if not message.server:
        return True
    return message.channel.name in settings[message.server.id]["enabledChannels"]

client.run(settings["client_secret"])