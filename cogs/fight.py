import discord
from discord.ext import commands
import asyncio
import psycopg2
import random
from func import * 
import os

DB_NAME= os.environ["DB_NAME"]
DB_USER=os.environ["DB_USER"]
DB_PASS= os.environ["DB_PASS"]
DB_HOST= os.environ["DB_HOST"]
DB_PORT= "5432"





activeChannels = []

class Fight (commands.Cog):
    def __init__(self,client):
        self.client = client
        

    @commands.command(aliase=['duel','challenge'])
    async def fight(self,ctx,enemy:discord.Member):
        Challenger= ctx.message.author
        ChallengerID= ctx.message.author.id
        enemyID= enemy.id
        entry_check_and_create(ChallengerID)
        entry_check_and_create(enemyID)
        channel = ctx.message.channel
        channelState= checkChannel (channel)
        if channelState == "False":
            activeChannels.append(channel)
            
            
            ChallengerHP= get_maxhp(ChallengerID)
            
            EnemyHP=get_maxhp(enemyID)

            
            def CheckAccept(message):
                message.content= message.content.lower()
                return message.content=="accept" and message.author==enemy
            
            await ctx.send(f"{enemy.mention} {ctx.message.author.name} has invited you to a duel!Type `accept` in chat to accept!")
            try:
                await self.client.wait_for('message',check=CheckAccept,timeout=30)
            
            
                
                #GameState= "Started"
                firstMove=["author","enemy"]
                turn=random.choices(firstMove)
                await ctx.send("Acccepted! The game will start in 5 seconds. Get ready!")
                embed=discord.Embed(
                    colour=discord.Colour.orange(),
                    title="Hit Points!"
                )
                embed.add_field(name=f"{Challenger.name}'s HP",value=ChallengerHP)
                embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
                await ctx.send(embed=embed)
                await asyncio.sleep(5)
                i= 1
                while ChallengerHP > 0 and EnemyHP>0:
                    
                    i +=1 
                    if turn=="author":
                        primary,secondary= getLoadout(ChallengerID)
                        await ctx.send(f"{Challenger.mention} make your move! You can either use your `{primary}` by typing `primary` or `{secondary}` by typing `secondary`")
                        def CheckChallengerMessage(message):
                            fightMoves= ['primary','secondary']
                            
                            return message.content.lower() in fightMoves and message.author == Challenger
                        try:
                            fightMove= await self.client.wait_for('message',check=CheckChallengerMessage,timeout=30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{Challenger.name} didn't respond in time!")
                            ChallengerHP = 0
                            break
                        fightMove.content= fightMove.content.lower()
                        if fightMove.content=="primary":
                            damage,Weapon,state= get_primary(ChallengerID)
                        elif fightMove.content == "secondary":
                            damage,Weapon,state= get_secondary(ChallengerID)
                        
                
                     
                        EnemyHP = EnemyHP - damage
                        if EnemyHP < 0:
                            EnemyHP = 0
                        embed = challengerHit (enemy,Challenger,damage,ChallengerHP,EnemyHP,Weapon,state)
                        await ctx.send(embed=embed)
                        turn = "enemy"
                        
                    else:
                        primary,secondary= getLoadout(enemyID)
                        await ctx.send(f"{enemy.mention} make your move! You can either use your `{primary}` by typing `primary` or `{secondary}` by typing `secondary`")
                        def CheckEnemyMessage(message):
                            
                            fightMoves = ['primary','secondary']
                            return message.content.lower() in fightMoves and message.author==enemy
                        try:
                            fightMove =await self.client.wait_for('message',check=CheckEnemyMessage,timeout= 30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{enemy.name} didn't respond in time!")
                            EnemyHP = 0
                            break
                        fightMove.content= fightMove.content.lower()
                        if fightMove.content=="primary":
                            damage,Weapon,state= get_primary(enemyID)
                        elif fightMove.content == "secondary":
                            damage,Weapon,state= get_secondary(enemyID)

                        
                        ChallengerHP = ChallengerHP - damage
                        if ChallengerHP < 0:
                            ChallengerHP = 0
                        embed = enemyHit (enemy,Challenger,damage,ChallengerHP,EnemyHP,Weapon,state)
                        await ctx.send(embed=embed)
                        turn="author"
                        
                        
                        
                    
                if ChallengerHP > EnemyHP :
                    await ctx.send(f"{Challenger.mention} won with {ChallengerHP} hp remaining.")
                    winnerStatUpdater(ChallengerID)
                    lossStatUpdater(enemyID)
                    await ctx.send(f"{Challenger.mention} You won! You get 50 gold and +2 max hp.")
                    await ctx.send(f"{enemy.mention} You lost! Your max hp has gone down by -1.")
                else:
                    await ctx.send(f"{enemy.mention} won with {EnemyHP} hp remaining.")
                    winnerStatUpdater(enemyID)
                    lossStatUpdater(ChallengerID)
                    await ctx.send(f"{enemy.mention} You won! You get 50 gold and +2 max hp.")
                    await ctx.send (f"{Challenger.mention} You lost! Your max hp has gone down by -1.")
                activeChannels.remove(channel)
            except asyncio.TimeoutError:
                await ctx.send(f"{enemy.mention} didn't accept in time! Pfft.")
                
                activeChannels.remove(channel) 
    
        else:
            await ctx.send("There is already an ongoing fight in this channel. Please use another channel.")

    










def setup(client):
    client.add_cog(Fight(client))
