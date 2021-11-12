# My lightweight discord backup bot.
# author Nicky (@starmaid#6925)
# created 12/04/2019 hbd rolal
# edited 11/11/2021

import discord
from discord.ext import commands
import asyncio
import logging

logging.basicConfig(level=logging.ERROR)

from datetime import datetime
from dateutil import parser
import time
import random
from random import choice
import json
import feedparser
import requests
import os


class Bot(commands.Bot):
    activity = 'meow! :3help'
    logoff_msg = 'logging off'

    def __init__(self):
        # This is the stuff that gets run at startup
        super().__init__(command_prefix=':3',self_bot=False,activity=discord.Game(self.activity))
        self.remove_command('help')
        self.add_command(self.help)
        self.add_command(self.refresh)
        self.add_command(self.about)
        self.add_command(self.quit)
        self.add_command(self.tvb)
        self.add_command(self.p)
        
        self.read_token()
        self.load_config()

        if self.token is None:
            print(str(datetime.now()) + ': Could not start server due to missing files')
            pass
        else:
            super().run(self.token)


    def read_token(self):
        self.token = None
        try:
            with open('./token.txt','r') as fp:
                self.token = fp.readlines()[0].strip('\n')
        except:
            print(str(datetime.now()) + ': Token file not found')


    


    @commands.command(pass_context=True)
    async def help(ctx):
        #this is the help command.
        cmd = ctx.message.content.lower().split()
        l = len(cmd)

        if l == 1:
            # no params, just plain help
            help_msg = '```:3 MUTIE BOT :3\n' + \
                'meow meow meow meow meow ' + \
                'meow meow :3' + \
                '\nusage:          :3command [params]*' + \
                '\n --- availible commands ---' + \
                '\n:3help                shows this message' + \
                '\n:3about               shows an about message for the bot' + \
                '\n:3quit                shuts down the bot (only works for starmaid)'

        else:
            help_msg = '```help parameters not recognized.'

        help_msg += '```'
        await ctx.send(help_msg)
        return


    @commands.command(pass_context=True)
    async def about(ctx):
        """send an about message"""
        global server_conf
        global rss_conf

        msg = '```<./> DSN BOT <./>' + \
            '\nInspired by the Deep Space Network, run by JPL in Pasadena, CA.' + \
            '\nMade by @starmaid#6925. Contact me with questions.' + \
            '\nGithub: https://github.com/starmaid/dsnbot' + \
            '\nCurrently in ' + str(len(server_conf.keys())) + ' servers' + \
            '\nWatching ' + str(len(rss_conf['rss'].keys())) + ' rss feeds and ' + \
            str(len(rss_conf['custom'].keys())) + ' custom feeds' + \
            '```'

        await ctx.send(msg)
        return


    async def on_guild_join(guild):
        # would love to say hi hehe
        

    @commands.command(pass_context=True)
    async def p(ctx):
        """Proxy the message through dsnbot. gives me a cool leg up on the roleplay"""

        if str(ctx.message.author) == 'starmaid#6925':
            await ctx.send(" ".join(ctx.message.content.split()[1:]))
            await ctx.message.delete()
        else:
            await ctx.send("`I DIDNT SAY THAT`")
        return  


    @commands.command(pass_context=True)
    async def backup(ctx):
        # backs up the server. whole thing. idiot.

        print("oh god, someone called backup...")

        

        guild = ctx.guild
        channels = guild.channels
        for c in channels:
            if not isinstance(c, discord.TextChannel):
                channels.remove(c)

        rootfolder = "../" + guild.name + " " + str(time.time()).split('.')[0]

        
        # make a folder for the backup
        os.makedirs(os.path.dirname(), exist_ok=True)
        
        counter = 0

        for chan in channels:
            after = datetime.datetime(2015, 5, 13) # fun fact, thats discords public release
            year = 2015

            async for message in chan.history(limit=1, after=after, oldest_first=True):
                # see how old the channel is, and start at that year
                print(message.created_at)
                year = message.created_at.year
            
            if year < datetime.datetime.now().year():
                print("write this")

            fname = rootfolder + chan.category.name + "/" + chan.name + "/" + year + ".txt"

            os.makedirs(os.path.dirname(fname), exist_ok=True)
            with open(fname, "w") as file:
                try:
                    async for message in chan.history(limit=None, after=after, oldest_first=True):
                        text = message.created_at.isoformat(sep=" ", timespec='minutes') + \
                                " [" + message.author.name + "]: " + message.clean_content
                        text = text.encode("ascii", errors="ignore").decode()
                        for pic in message.attachments:
                            text += " [ " + pic.url + " ]"
                        counter += 1
                        if counter%200 == 0:
                            print(chan.name + " " + message.clean_content[0:20])
                        file.write(text + "\n")
                except:
                    print("--- failed channel: " + chan.name)
                    pass



    async def on_command_error(self, ctx, error):
        """Handle commands that are not recognized so it stops printing to console"""
        if type(error) is commands.CommandNotFound:
            msg = "`command not recognized.`"
            await ctx.send(msg)
    


    @commands.command(pass_context=True)
    async def quit(ctx):
        # quits the bot.
        if str(ctx.message.author) == 'starmaid#6925':
            await ctx.send(ctx.bot.logoff_msg)
            await ctx.bot.close()
            quitBrowser()
        else:
            await ctx.send('`you do not have permission to shut me down.`')
        
        print(str(datetime.now()) + ': Shutting down')
        return




if __name__ == '__main__':
    Bot()
