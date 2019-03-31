import discord
import asyncio
import logging
from discord.ext import commands
import json
import urllib.request
import os
import time

TOKEN = json.load(open("token.json"))["token"]

logging.basicConfig(level=logging.INFO)

cached_avatars_timeout = dict()
if not os.path.isdir("cache"):
    os.mkdir("cache")
else:
    for x in os.listdir("cache"):
        os.unlink("cache/" + x)

bot = commands.Bot(command_prefix="k-", description="Kartof-Bot Rewrite von Jerry")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name + "#" + bot.user.discriminator)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "kartof fahren" in message.content.lower():
        await bot.send_message(message.channel, "fahren kartof")

    elif "fahren kartof" in message.content.lower():
        await bot.send_message(message.channel, "kartof fahren")

    elif "thema kartoffeln" in message.content.lower():
        await bot.send_message(message.channel, "thema es heißt kartof")

    elif "kartof" in message.content.lower():
        await bot.send_message(message.channel, "kartof")

    elif "fahren" in message.content.lower():
        await bot.send_message(message.channel, "fahren")

    elif "kartowof" in message.content.lower():
        await bot.send_message(message.channel, "kartuwuf")

    await bot.process_commands(message)

bot.remove_command("help")


@bot.command()
async def help():
    await bot.say("Willkommen zu **KARTOF-Rewrite**, wählen Sie aus den folgenden Sprachweisen aus: \n `kartof` - kartof \n `fahren` - fahren \n `kartof fahren` - fahren kartof \n `fahren kartof` - eben genau so \n `kartowof` - kartuwuf \n `k-help` - was du gerade tipptest \n `k-handwritinghelp` – das kann man eh nicht lesen \n `k-info` - mehr informationen zu diesem bot \n `k-rank` - zeigt deinen rang auf diesem server an \n `k-color` - simples kartofgelb in einem kaputten embed \n `k-userinfo` - wer bist du? \n `k-avatar` - zeigt dein wunderschönes gesicht uwu \n")


@bot.command()
async def handwritinghelp():
    await bot.say("https://i.imgur.com/ddjXRmO.jpg")


@bot.command()
async def info():
    await bot.say("""
Ich bin **KARTOF-Rewrite**, wurde von Jerrynicki ID: 346295434546774016 kartoft und es ist ein Wunder, dass ich gerade funktioniere. Auch sonst bin ich absolut nutzlos.
 Falls du einen Server brauchst, um dies zu bestätigen, geh hier:
 https://discord.gg/H42pZsu
 falls du Kartof-Rewrite auf deinem Server haben möchtest, geh hier:
 <https://leo.immobilien/de/Mecklenburg-Vorpommern/Schwerin/Friedrichplatz/43>""")


@bot.command()
async def rank():
    await bot.say("du bist Nummer eins :yellow_heart:")


@bot.command(pass_context=True)
async def color(ctx):
    embed = discord.Embed(title="Kartof-Gelb", description="#ffd726", color=0xffd726)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def userinfo(ctx):
    await bot.say("Du bist **" + ctx.message.author.name + "**, und laut deiner ID schälst du **" + ctx.message.author.id + "** Kartofs.")


@bot.command(pass_context=True)
async def avatar(ctx, *user: discord.Member):
    try:
        if not (not user):
            ctx.message.author = user[0]

        if not os.path.isfile("cache/" + ctx.message.author.id + ".png"):
            if ctx.message.author.avatar_url == "":
                await bot.say("Dieser Nutzer hat keinen eigenen Avatar!")
                return
            
            req = urllib.request.Request(ctx.message.author.avatar_url,
                                         headers={"User-Agent": "Mozilla/5.0"})
            recvd = urllib.request.urlopen(req, timeout=10).read()

            with open("cache/" + ctx.message.author.id + ".png", "wb") as file:
                file.write(recvd)

            cached_avatars_timeout[ctx.message.author.id] = 200 

        await bot.send_file(ctx.message.channel, "cache/" + ctx.message.author.id + ".png")

    except Exception as exc:
        await bot.say("Fehler beim Herunterladen des Avatars: " + str(exc))

async def avatar_delete():
    while True:
        try:
            await asyncio.sleep(5)
            to_delete = []
            for x in cached_avatars_timeout:
                cached_avatars_timeout[x] -= 5
                if cached_avatars_timeout[x] <= 0:
                    to_delete.append(x)

            for x in to_delete:
                if os.path.isfile("cache/" + x + ".png"):
                    os.unlink("cache/" + x + ".png")
                    del cached_avatars_timeout[x]

            # print(cached_avatars_timeout)

        except Exception as exc:
            print("avatar_delete: " + str(exc))

bot.loop.create_task(avatar_delete())

bot.run(TOKEN)
