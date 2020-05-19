import discord
from discord.ext import commands,tasks
from datetime import datetime
import json
import asyncio
import random



class Events(commands.Cog):
    def __init__(self,client):
        self.client=client

   
       


    @commands.Cog.listener()
    async def on_ready (self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Fighting"))
        print("Bot is ready")

    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        print(f"{member} has joined a server.")
       

   

        
        
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f"{member} has left a server.")



    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
       banmessage = "ban message"
       await user.send(f'{banmessage}')

    @commands.Cog.listener()
    async def on_guild_join(self,guild:discord.guild):
        channel= discord.utils.get(guild.text_channels,name="general")
        embed=discord.Embed(
            colour=discord.Colour.green(),
            title="Hi",
            description=f"Hello! Thank you for adding me to {guild.name}. I am a new bot so please expect a few bugs.\n DM `GenVenom#3394` if you encounter any bugs and they will be fixed.\n My prefix is `f/`. To get started, please run the `f/help` command.\n Have fun!"
        )
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Events(client))

