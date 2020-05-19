import discord
from discord.ext import commands,tasks
import psycopg2
from func import *
import os

DB_NAME= os.environ["DB_NAME"]
DB_USER=os.environ["DB_USER"]
DB_PASS= os.environ["DB_PASS"]
DB_HOST= os.environ["DB_HOST"]
DB_PORT= "5432"



conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userdata (userid TEXT, maxHP INT,bal INT, wins INT,losses INT,wprimary TEXT, wsecondary TEXT, potions TEXT)")

conn.commit()
conn.close()
print("DB is connected!")


class Shop(commands.Cog):
    def __init__(self,client):
        self.client = client
        

    @commands.command()
    async def shop(self,ctx):
        embed=discord.Embed(
            colour= discord.Colour.green(),
            title= "Buy weapons and items to use in battles here!"
        )
        embed.set_author(name="Shop")
        embed.add_field(name="Primary Weapons", value= "Claymore - 100\n Light Sword - 200 \n Heavy Sword - 300 \n Bow - 400\n Dual Sword- 500\n Spear- 600",inline=False)
        embed.add_field(name="Secondary Weapons", value ="Dagger -50\n Khukuri - 70\n Throwing Knives - 90\n Poison Dart - 100",inline=False)
        embed.add_field(name="Potions",value ="Small health pot -25\n Big Health pot - 50\n Instant damage Potion-60 \n Potion of Weakness - 75\n Potion of immunity- 250\n",inline=False) 
        await ctx.send(embed=embed)

    @commands.command()
    async def buy (self,ctx,*,items):
        items= itemNameSorter(items)
        primary=['claymore','light_sword','heavy_sword','bow','dual_sword','spear']
        secondary= ['dagger','khukuri','throwing_knives','poison_dart']
        potions= ['small_health_pot','big_health_pot','instant_damage_pot','potion_of_weakness','potion_of_immunity']
        primaryPrices={
            'claymore': 100,
            'light sword':200,
            'heavy sword':300,
            'bow':400,
            'dual sword':500,
            'spear':600 ,
        }

        secondaryPrices={
            'dagger':50,
            'khukuri':70,
            'throwing_knives':90,
            'poison_dart':100
        }

        potionPrices={
            'small_health_pot': 25,
            'big_health_pot':50,
            'instant_damage_pot':60,
            'potion_of_weakness':75,
            'potion_of_immunity':250
        }
        buyerBalance = get_bal(ctx.message.author.id)

        if items in primary or items in secondary or items in potions:
            conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
            c=conn.cursor()
            entry_check_and_create(ctx.message.author.id)
            if items in primary:
                if buyerBalance >= primaryPrices[items]:
                    c.execute(f"UPDATE userdata SET wprimary='{items}' where userid='{ctx.message.author.id}'")
                    conn.commit()
                    c.close()
                    conn.close()
                    await ctx.send("Item has been added to your inventory")
                    newBalance = buyerBalance - primaryPrices[items]
                    balanceAdjuster(ctx.message.author.id,newBalance)
                else:
                    await ctx.send(f"You don't have enough balance to buy a {items}.")
            elif items in secondary:
                if buyerBalance >= secondaryPrices[items]:
                    c.execute(f"UPDATE userdata SET wsecondary='{items}' where userid='{ctx.message.author.id}'")
                    conn.commit()
                    c.close()
                    conn.close()
                    await ctx.send("Item has been added to your inventory")
                    newBalance= buyerBalance - secondaryPrices[items]
                    balanceAdjuster(ctx.message.author.id,newBalance)
                else:
                    await ctx.send(f"You don't have enough money to buy a {items}")
            else:
                if buyerBalance >= potionPrices[items]:
                    c.execute(f"UPDATE userdata SET potions='{items}' where userid='{ctx.message.author.id}'")
                    conn.commit()
                    c.close()
                    conn.close()
                    await ctx.send("Item has been added to your inventory")
                    newBalance= buyerBalance - potionPrices[items]
                    balanceAdjuster(ctx.message.author.id,newBalance)
                else:
                    await ctx.send(f"You dont have enough balance to buy {items}")
        else:
            await ctx.send("Item not found.")

    
    










def setup(client):
    client.add_cog(Shop(client))
