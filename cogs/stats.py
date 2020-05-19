import discord
from discord.ext import commands,tasks
from func import *


class Stats(commands.Cog):
    def __init__(self,client):
        self.client= client

    @commands.command()
    async def bal(self,ctx,user:discord.Member=0):
        if user==0:
            user= ctx.message.author
        entry_check_and_create(user.id)
        Balance  = get_bal(user.id)

        embed=discord.Embed(
            colour=discord.Colour.gold(),
            title = f"**{user}'s balance**",
            description= f"You currently have ${Balance}."
        
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693104930717827092/693104965480087672/money_bag.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def maxhp(self,ctx,user:discord.Member=0):
        if user==0:
            user= ctx.message.author
        entry_check_and_create(user.id)
        maxHP  = get_maxhp(user.id)

        embed=discord.Embed(
            colour=discord.Colour.gold(),
            title = f"**{user}'s max hp**",
            description= f"{user.name} currently has {maxHP} HP."
        
        )
        #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693104930717827092/693104965480087672/money_bag.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self,ctx,user:discord.Member=0):
        if user == 0:
            user = ctx.message.author
        entry_check_and_create (user.id)
        maxHP= get_maxhp (user.id)
        balance = get_bal(user.id)
        wins = get_wins(user.id)
        losses=get_loss(user.id)
        primary,secondary = getLoadout(user.id)
        primary= itemNameFixer(primary)
        secondary= itemNameFixer(secondary)
        embed=discord.Embed(
            colour= discord.Colour.blue(),
            title=f"{user.name}'s Stats",
            description= "The follwing stats are global."
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Starting HP  ",value=maxHP)
        embed.add_field(name="Balance",value=balance)
        embed.add_field(name="Wins",value=wins)
        embed.add_field(name="Losses",value=losses,)
        embed.add_field(name="Primary Weapon",value=primary)
        embed.add_field(name="Secondary Weapon",value=secondary)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Stats(client))

