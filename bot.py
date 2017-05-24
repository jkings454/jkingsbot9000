# This is a complete rewrite of the bot
# Hopefully more sane and understandable than the last one.
import json
import random
import discord
import asyncio

import requests

import config

from util.logger import  Logger
from util.command_parser import *
from util.timeutils import *

myconf = config.Config()
logger = Logger()

client = discord.Client()

TIG_ID = "291451818712629249"
KINGS_ID = "305438956701614081"

@client.event
async def on_ready():
    logger.log_event("Logged in as " + client.user.name)
    await client.change_presence(game=discord.Game(name='something gay'))

@client.event
async def on_server_join(server):
    myconf.create_empty_dict(server.id)
    myconf.settings[server.id]["prefix"] = "!" # initialize default prefix
    myconf.settings[server.id]["timeFormat"] = "%y/%m/%d [%H:%M:%S]"
    myconf.settings[server.id]["enabledChannels"] = []
    myconf.save()
    logger.log_event("Joined server " + server.name)

@client.event
async def on_message(message):

    if "i'm gay" in message.content.lower():
        await client.add_reaction(message, "🏳️‍🌈")

    try:
        parser = CommandParser(myconf.settings[message.server.id]["prefix"])
    except AttributeError:
        parser = CommandParser("!")

    parsed = parser.parse(message.content)

    if not parsed: return


    # Help command invoked
    if parsed.command == "help":
        # Gives users text so that they know how the bot works.
        if parsed.args:
            if parsed.args[0] == "time":
                await client.send_message(message.channel,
                                          "For a list of supported timezones, please see " +
                                          "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
                return

        fo = open("help.txt")
        text = fo.read()
        fo.close()

        await client.send_message(message.channel, text)

    elif parsed.command == "enable":
        # Adds the channel to the active channels.
        if not is_admin(message.author, message.channel):
            await client.send_message(message.channel,
                                      "You don't have permission to run this command. "
                                      "Please have an administrator run this command.")
            return

        if message.channel.id in myconf.settings[message.server.id]["enabledChannels"]:
            await client.send_message(message.channel, "This channel is already enabled!")
            return

        myconf.settings[message.server.id]["enabledChannels"].append(message.channel.id)
        myconf.save()
        logger.log_event("Updated settings for \"" + message.server.name + "\"")
        await client.send_message(message.channel, "This channel has been added to your active channels!")



    elif parsed.command == "disable":
        # removes the channel from the enabled chanels
        if not is_admin(message.author, message.channel):
            await client.send_message(message.channel,
                                      "You don't have permission to run this command. Please have an administrator"
                                      "run this command.")
            return

        if not message.channel.id in myconf.settings[message.server.id]["enabledChannels"]:
            await client.send_message(message.channel, "This channel isn't enabled!")
            return


        myconf.settings[message.server.id]["enabledChannels"].remove(message.channel.id)
        myconf.save()
        logger.log_event("Updated settings for \"" + message.server.name + "\"")
        await client.send_message(message.channel, "This channel is no longer in your enabled channels")

    elif parsed.command == "test":
        if not is_enabled_channel(message.channel, myconf.settings):
            await client.send_message(message.channel, "This channel isn't enabled. "
                                                       "Please have an administrator run !enable")
            return

        if message.author.id == TIG_ID:
            await client.send_message(message.channel, "eyy bb ;)")
        elif message.author.id == KINGS_ID:
            await client.send_message(message.channel, ":crown: All Hail " + message.author.mention + "! :crown:")
        else:
            await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif parsed.command == "gay":
        if not is_enabled_channel(message.channel, myconf.settings):
            await client.send_message(message.channel, "This channel isn't enabled. "
                                                       "Please have an administrator run !enable")
            return

        await client.send_message(message.channel, random.choice(myconf.settings["gay_things"]))

    elif parsed.command == "time":
        if type(message.channel) == discord.PrivateChannel:
            tf = "%y%m%d [%H:%M:%S]"
        else:
            tf = myconf.settings[message.server.id]["timeFormat"]
        if parsed.args:
            for arg in parsed.args:
                try:
                    curtime = current_time_for_timezone(arg, tf)
                except:
                    if arg == "tig":
                        curtime = current_time_for_timezone("Australia/Sydney", tf)

                    elif arg == "kings":
                        curtime = current_time_for_timezone("US/Mountain", tf)

                    else:
                        await client.send_message(message.channel,
                                                  "\"" + arg + "\" is not a valid time zone")
                        continue

                await client.send_message(message.channel, "The current time for " + arg +
                                          " is `" + curtime + "`")
        else:
            curtime = current_utc_time(tf)
            await client.send_message(message.channel, "it is `" + curtime + "` UTC")

    elif parsed.command == "quote":
        if not is_enabled_channel(message.channel, myconf.settings):
            await client.send_message(message.channel, "This channel isn't enabled. "
                                                       "Please have an administrator run !enable")
            return

        await client.send_typing(message.channel)
        await client.send_message(message.channel, get_random_quote())



# Helper methods which may or may not be changed in the future

def is_admin(user, channel):
    if not channel:
        return True

    return user.permissions_in(channel).administrator

def get_enabled_channels(server, settings):
    list = [channel for channel in server.channels if (channel.id in settings[server.id]["enabledChannels"])]
    return list

def is_enabled_channel(channel, settings):
    if type(channel) == discord.PrivateChannel:
        # We're in a PM or a group chat. There is no channel.
        return True

    return channel.id in settings[channel.server.id]["enabledChannels"]

def get_random_quote():
    quote = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
    quote = json.loads(quote.text)

    message = "\"" + quote["quoteText"] + "\""
    message += "\n\n -- " + quote["quoteAuthor"]

    return message

client.run(myconf.settings["client_secret"])