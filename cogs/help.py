import discord
from discord.ext import commands,tasks

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def help(self,ctx):
        embed=discord.Embed(
            colour=discord.Colour.green(),
            title="Help",
            description="Welcome to Fitebot! A discord bot that allows you to fight your friends using various weapons.\n The bot has a progressive system where you progress as you interact with the bots by dueling other players. \n Below is a complete list of commands with their explanations!"
        )
        embed.add_field(name="Commands & their description",value="fight [`@user`] = Challenges a user to a duel \n shop = Opens the shop menu \n buy [`itemname`]= Allows you to buy an item from the shop \n bal [`Optional: @user`] = Shows you your/others current balance \n stats[`Optional: @user`]= Shows your/others current stats (Win/Loss) \n maxhp [`Optional: @user`]= Shows your/others current max hp")
        await ctx.send(embed=embed)

    @commands.command(aliases=['wi'])
    async def weaponinfo(self,ctx):
        embed=discord.Embed(
            colour = discord.Colour.blue(),
            title="Weapon accuracy and damage info!",
            description = "You can only old one of each weapon at a time. Buying a new weapon will replace the old one.\n The following weapon damage and accuracy values are subject to change to maintain balance."
        )
        embed.set_author(name="Patch 1.0")
        embed.add_field(name="Primary Weapons",value="Wooden sword : Accuracy -> 100%  Damage -> 8-10 \n Light Sword: Accuracy ->95%  Damage -> 9-12 \n Claymore: Accuracy ->90%  Damage -> 13-16 \n Dual Sword: Accuracy ->85%  Damage -> 14-17 \n Heavy Sword: Accuracy ->73%  Damage -> 15-19 \n Bow: Accuracy ->60%  Damage -> 18-23 \n Spear: Accuracy ->50%  Damage -> 23-30 \n",inline=False)
        embed.add_field(name="Secondary Weapon",value ="All secondary weapons have 100% Accuracy \n Wooden Dagger: Damage -> 2-4 \n Dagger: Damage -> 5-7 \n Khukuri: Damage -> 6-9 \n Throwing Knives: Damage-> 9-14 \n Poison Dart: Damage ->12-16",inline=False)
        embed.add_field(name="Potions",value="Potions are an upcoming feature. They will be added in the next patch.",inline=False)
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Help(client))