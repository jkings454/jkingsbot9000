import discord
import asyncio
import datetime
import pytz
import json

client = discord.Client()

fo = open("settings.json")
settings = json.load(fo)
fo.close()

TIG_ID = "291451818712629249"
KINGS_ID = "305438956701614081"

@client.event
async def on_message(message):
    if message.content.startswith("!test"):
        if message.author.id == TIG_ID:
            tmp = await client.send_message(message.channel, "eyy bb ;)")
        elif message.author.id == KINGS_ID:
            tmp = await client.send_message(message.channel, "All Hail " + message.author.mention + "!")
        else:
            tmp = await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.startswith("!time"):
        tokenized = message.content.split()
        
        
        
        if (len(tokenized) > 1):
            try:
                #this should be a timezone
                #hopefully
                tz = pytz.timezone(tokenized[1])
                curtime = datetime.datetime.now(tz)
                stringtime = curtime.strftime("%Y/%m/%d %H:%M:%S")
                timestr = message.author.mention + ", the current time in " + tokenized[1] + " is `" + stringtime + "`"
            except:
                timestr = "That timezone is unsupported."
            
        else:
            curtime = datetime.datetime.utcnow()
            stringtime = curtime.strftime("%Y/%m/%d %H:%M:%S UTC")
            timestr = message.author.mention + ", the current time is `" + stringtime + "`"
            
        tmp = await client.send_message(message.channel, timestr)

    elif message.content.startswith("!tigtime"):
        au = pytz.timezone("Australia/Sydney")
        curtime = datetime.datetime.now(au)
        stringtime = curtime.strftime("%Y/%m/%d %H:%M:%S")

        tmp = await client.send_message(message.channel, "it is `" + stringtime + "` for tigrriis")

    elif message.content.startswith("!kingstime"):
        ut = pytz.timezone("US/Mountain")
        curtime = datetime.datetime.now(ut)
        stringtime = curtime.strftime("%Y/%m/%d %H:%M:%S")

        tmp = await client.send_message(message.channel, "it is `" + stringtime + "` for jkings")
            
client.run(settings["client_secret"])