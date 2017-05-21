import discord
import asyncio

import timeutils

import datetime
import pytz
import json

import requests

client = discord.Client()

fo = open("settings.json")
settings = json.load(fo)
fo.close()

TIG_ID = "291451818712629249"
KINGS_ID = "305438956701614081"

def log_event(message):
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] "
    + message)

@client.event
async def on_ready():
    log_event("logged in as:\n %s\n %s\n-------" % (client.user.name, client.user.id))

@client.event
async def on_message(message):
    #TODO: Create a handler for these, rather than doing this

    if message.content.startswith("!test"):
        log_event("!test invocation from %s in server [%s]" % (message.author.name, message.server))
        if message.author.id == TIG_ID:
            await client.send_message(message.channel, "eyy bb ;)")
        elif message.author.id == KINGS_ID:
            await client.send_message(message.channel, "All Hail " + message.author.mention + "!")
        else:
            await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.startswith("!time"):
        log_event("!time invocation from " + message.author.name + " in server [" + message.server.name + "]")
        tokenized = message.content.split()

        if (len(tokenized) > 1):
            try:
                #this should be a timezone
                #hopefully
                timestr = message.author.mention + ", the current time in " \
                          + tokenized[1]  + " is `" \
                          + timeutils.current_time_for_timezone(tokenized[1]) + "`"
            except:
                timestr = "That timezone is unsupported."
            
        else:
            stringtime = timeutils.current_utc_time()
            timestr = message.author.mention + ", the current time is `" + stringtime + "`"
            
        await client.send_message(message.channel, timestr)

    elif message.content.startswith("!tigtime"):
        au = pytz.timezone("Australia/Sydney")
        stringtime = timeutils.current_time_for_timezone(au)

        await client.send_message(message.channel, "it is `" + stringtime + "` for tigrriis")

    elif message.content.startswith("!kingstime"):
        ut = pytz.timezone("US/Mountain")
        stringtime = timeutils.current_time_for_timezone(ut)

        await client.send_message(message.channel, "it is `" + stringtime + "` for jkings")

    elif message.content.startswith("!quote"):
        await client.send_message(message.channel, get_random_quote())

    elif message.content.startswith("!help"):
        fo = open("help.txt")
        content = fo.read()

        await client.send_message(message.channel, content)


def get_random_quote():
    quote = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
    quote = json.loads(quote.text)

    message = "\"" + quote["quoteText"] + "\""
    message += "\n\n -- " + quote["quoteAuthor"]

    return message

client.run(settings["client_secret"])